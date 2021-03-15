from odoo import models, api


class ReportAccountFinancialReport(models.Model):
    _inherit = "account.financial.html.report"

    @api.model
    def _get_financial_line_report_line(self, options, financial_line, solver, groupby_keys):
        ''' Create the report line for an account.financial.html.report.line record.
        :param options:             The report options.
        :param financial_line:      An account.financial.html.report.line record.
        :param solver_results:      An instance of the FormulaSolver class.
        :param groupby_keys:        The sorted encountered keys in the solver.
        :return:                    The dictionary corresponding to a line to be rendered.
        '''
        results = solver.get_results(financial_line)['formula']

        is_leaf = solver.is_leaf(financial_line)
        has_lines = solver.has_move_lines(financial_line)

        # Update Perubahan isd_pit_source
        has_lines = True

        has_something_to_unfold = is_leaf and has_lines and bool(financial_line.groupby)

        # Compute if the line is unfoldable or not.
        is_unfoldable = has_something_to_unfold and financial_line.show_domain == 'foldable'

        # Compute if the line is unfolded or not.
        # /!\ Take care about the case when the line is unfolded but not unfoldable with show_domain == 'always'.
        if not has_something_to_unfold or financial_line.show_domain == 'never':
            is_unfolded = False
        elif financial_line.show_domain == 'always':
            is_unfolded = True
        elif financial_line.show_domain == 'foldable' and financial_line.id in options['unfolded_lines']:
            is_unfolded = True
        else:
            is_unfolded = False

        # Standard columns.
        columns = []
        for key in groupby_keys:
            amount = results.get(key, 0.0)
            columns.append(
                {'name': self._format_cell_value(financial_line, amount), 'no_format': amount, 'class': 'number'})

        # Growth comparison column.
        if self._display_growth_comparison(options):
            columns.append(self._compute_growth_comparison_column(options,
                                                                  columns[0]['no_format'],
                                                                  columns[1]['no_format'],
                                                                  green_on_positive=financial_line.green_on_positive
                                                                  ))

        # Debug info columns.
        if self._display_debug_info(options):
            columns.append(self._compute_debug_info_column(options, solver, financial_line))

        financial_report_line = {
            'id': financial_line.id,
            'name': financial_line.name,
            'level': financial_line.level,
            'class': 'o_account_reports_totals_below_sections' if self.env.company.totals_below_sections else '',
            'columns': columns,
            'unfoldable': is_unfoldable,
            'unfolded': is_unfolded,
            'page_break': financial_line.print_on_new_page,
            'action_id': financial_line.action_id.id,
        }

        # Custom caret_options for tax report.
        if self.tax_report and financial_line.domain and not financial_line.action_id:
            financial_report_line['caret_options'] = 'tax.report.line'

        return financial_report_line

class AccountFinancialReportLine(models.Model):
    _inherit = "account.financial.html.report.line"

    def _compute_amls_results(self, options_list, sign=1):
        ''' Compute the results for the unfolded lines by taking care about the line order and the group by filter.

        Suppose the line has '-sum' as formulas with 'partner_id' in groupby and 'currency_id' in group by filter.
        The result will be something like:
        [
            (0, 'partner 0', {(0,1): amount1, (0,2): amount2, (1,1): amount3}),
            (1, 'partner 1', {(0,1): amount4, (0,2): amount5, (1,1): amount6}),
            ...               |
        ]    |                |
             |__ res.partner ids
                              |_ key where the first element is the period number, the second one being a res.currency id.

        :param options_list:        The report options list, first one being the current dates range, others being the
                                    comparisons.
        :param sign:                1 or -1 to get negative values in case of '-sum' formula.
        :return:                    A list (groupby_key, display_name, {key: <balance>...}).
        '''
        self.ensure_one()
        params = []
        queries = []

        AccountFinancialReportHtml = self.financial_report_id
        horizontal_groupby_list = AccountFinancialReportHtml._get_options_groupby_fields(options_list[0])
        groupby_list = [self.groupby] + horizontal_groupby_list
        groupby_clause = ','.join('account_move_line.%s' % gb for gb in groupby_list)
        groupby_field = self.env['account.move.line']._fields[self.groupby]

        ct_query = self.env['res.currency']._get_query_currency_table(options_list[0])
        financial_report = self._get_financial_report()

        # Prepare a query by period as the date is different for each comparison.

        for i, options in enumerate(options_list):
            new_options = self._get_options_financial_line(options)
            line_domain = self._get_domain(new_options, financial_report)

            tables, where_clause, where_params = AccountFinancialReportHtml._query_get(new_options, domain=line_domain)


            queries.append('''
                SELECT
                    ''' + (groupby_clause and '%s,' % groupby_clause) + '''
                    %s AS period_index,
                    COALESCE(SUM(ROUND(%s * account_move_line.balance * currency_table.rate, currency_table.precision)), 0.0) AS balance
                FROM ''' + tables + '''
                JOIN ''' + ct_query + ''' ON currency_table.company_id = account_move_line.company_id
                WHERE ''' + where_clause + '''
                ''' + (groupby_clause and 'GROUP BY %s' % groupby_clause) + '''
            ''')


            if line_domain[0]:
                if line_domain[0][0] == "account_id.user_type_id":
                    strParamUser_type_id = ''
                    if isinstance(line_domain[0][2], list):
                        for objParam in line_domain[0][2]:
                            where_params.append(objParam)
                            if strParamUser_type_id != '': strParamUser_type_id += ','
                            strParamUser_type_id += '%s'
                    else:
                        where_params.append(line_domain[0][2])
                        strParamUser_type_id += '%s'

                    queries.clear()

                    queries.append('''
                            select account_id, period_index, sum(balance) as balance from (
                                SELECT
                                    ''' + (groupby_clause and '%s,' % groupby_clause) + '''
                                    %s AS period_index,
                                    COALESCE(SUM(ROUND(%s * account_move_line.balance * currency_table.rate, currency_table.precision)), 0.0) AS balance
                                FROM ''' + tables + '''
                                JOIN ''' + ct_query + ''' ON currency_table.company_id = account_move_line.company_id
                                WHERE ''' + where_clause + '''
                                ''' + (groupby_clause and 'GROUP BY %s' % groupby_clause) + '''
                                Union 
                                select aa.id as account_id, 0 AS period_index, 0 as balance from account_account aa
                                    JOIN ''' + ct_query + ''' ON currency_table.company_id = aa.company_id
                                where aa.user_type_id in (''' + strParamUser_type_id + ''') 
                            ) as MergerAll
                            group by account_id, period_index
                        ''')

                if line_domain[0][0] == "account_id.user_type_id.type":
                    where_params.append(line_domain[0][2])
                    queries.clear()

                    queries.append('''
                        select account_id, period_index, sum(balance) as balance from (
                            SELECT
                                ''' + (groupby_clause and '%s,' % groupby_clause) + '''
                                %s AS period_index,
                                COALESCE(SUM(ROUND(%s * account_move_line.balance * currency_table.rate, currency_table.precision)), 0.0) AS balance
                            FROM ''' + tables + '''
                            JOIN ''' + ct_query + ''' ON currency_table.company_id = account_move_line.company_id
                            WHERE ''' + where_clause + '''
                            ''' + (groupby_clause and 'GROUP BY %s' % groupby_clause) + '''
                            Union 
                            select aa.id as account_id, 0 AS period_index, 0 as balance from account_account aa
                                inner join account_account_type aat on aa.user_type_id = aat.id
                                JOIN ''' + ct_query + ''' ON currency_table.company_id = aa.company_id
                            where aat.type = %s 
                        ) as MergerAll
                        group by account_id, period_index
                    ''')


            params += [i, sign] + where_params

        # Fetch the results.
        # /!\ Take care of both vertical and horizontal group by clauses.

        results = {}

        financial_report._cr_execute(options_list[0], ' UNION ALL '.join(queries), params)
        for res in self._cr.dictfetchall():
            # Build the key.
            key = [res['period_index']]
            for gb in horizontal_groupby_list:
                key.append(res[gb])
            key = tuple(key)

            results.setdefault(res[self.groupby], {})
            results[res[self.groupby]][key] = res['balance']

        # Sort the lines according to the vertical groupby and compute their display name.
        if groupby_field.relational:
            # Preserve the table order by using search instead of browse.
            sorted_records = self.env[groupby_field.comodel_name].search([('id', 'in', tuple(results.keys()))])
            sorted_values = sorted_records.name_get()
        else:
            # Sort the keys in a lexicographic order.
            sorted_values = [(v, v) for v in sorted(list(results.keys()))]

        return [(groupby_key, display_name, results[groupby_key]) for groupby_key, display_name in sorted_values]