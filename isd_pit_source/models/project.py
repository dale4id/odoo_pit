# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools.misc import format_date
from datetime import timedelta, datetime, date

from odoo.tools.safe_eval import pytz


class ProjectTask(models.Model):
    _inherit = "project.task"



    otheruser_id = fields.One2many("project.task.otheruser", inverse_name='task_id')
    user_checking = fields.One2many("project.task.checkinguser", inverse_name='task_id')
    user_fixing = fields.One2many("project.task.fixinguser", inverse_name='task_id')

    stsonhold = fields.Selection([
            ('0', 'On Progress'),
            ('1', 'On Hold'),
            ('2', 'Done')
        ], string="Progress", default="0", required=True, tracking=True)
    default_code = fields.Many2one('product.unit', string="Product Unit")
    product_id = fields.Many2one('product.product', string="Product")
    name_seq_fs = fields.Char(string='Field Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    task_no = fields.Char(string='Task No', required=True, copy=False, readonly=True, index=True,
                          default=lambda self: _('New'))

    total_worksheet_product = fields.Float(
        'Total Wordksheet Product', compute='_compute_worksheet_isd')
    team_id = fields.Many2one(string='Helpdesk Team', related='helpdesk_ticket_id.team_id')

    #report LPU
    nama_lpu = fields.Char(
        'Nama LPU', compute='_compute_worksheet_isd')
    alamat_lpu = fields.Char(
        'Alamat LPU', compute='_compute_worksheet_isd')
    kota_lpu = fields.Char(
        'Kota LPU', compute='_compute_worksheet_isd')
    zipcode_lpu = fields.Char(
        'KodePos LPU', compute='_compute_worksheet_isd')
    code_lpu = fields.Char(
        'Unique LPU', compute='_compute_worksheet_isd')
    merk_lpu = fields.Char(
        'Merk LPU', compute='_compute_worksheet_isd')
    type_lpu = fields.Char(
        'Type LPU', compute='_compute_worksheet_isd')
    logo_lpu = fields.Char(
        'Logo LPU', compute='_compute_worksheet_isd')
    model_lpu = fields.Char(
        'Model LPU', compute='_compute_worksheet_isd')
    serial_lpu = fields.Char(
        'Serial LPU', compute='_compute_worksheet_isd')
    kategori_lpu = fields.Char(
        'Kategori LPU', compute='_compute_worksheet_isd')
    tanggal_lpu = fields.Char(
        'Tanggal LPU', compute='_compute_worksheet_isd')
    listrik_lpu = fields.Char(
        'Listrik LPU', compute='_compute_worksheet_isd')
    tegangan_lpu = fields.Char(
        'Tegangan LPU', compute='_compute_worksheet_isd')
    kabel_lpu = fields.Char(
        'Kabel Power LPU', compute='_compute_worksheet_isd')
    wiring_lpu = fields.Char(
        'Wiring LPU', compute='_compute_worksheet_isd')
    kapasitor_lpu = fields.Char(
        'Kapasitor LPU', compute='_compute_worksheet_isd')
    kompresor_lpu = fields.Char(
        'Kompressor LPU', compute='_compute_worksheet_isd')
    thermostat_lpu = fields.Char(
        'Thermostat LPU', compute='_compute_worksheet_isd')
    ballast_lpu = fields.Char(
        'Ballast LPU', compute='_compute_worksheet_isd')
    relay_lpu = fields.Char(
        'Relay LPU', compute='_compute_worksheet_isd')
    bunga_lpu = fields.Char(
        'Bunga Es LPU', compute='_compute_worksheet_isd')
    noreges_lpu = fields.Char(
        'No Reges LPU', compute='_compute_worksheet_isd')
    noreges_ganti_lpu = fields.Char(
        'No Reges Ganti LPU', compute='_compute_worksheet_isd')
    image_unit = fields.Binary(
        string="Image Unit", compute='_compute_worksheet_isd')
    image_rusak = fields.Binary(
        string="Image Rusak", compute='_compute_worksheet_isd')
    analisa_lpu = fields.Char(
        'Hasil Analisa LPU', compute='_compute_worksheet_isd')
    akhir_lpu = fields.Char(
        'Hasil Akhir LPU', compute='_compute_worksheet_isd')
    product1_lpu = fields.Char(
        'Product1 LPU', compute='_compute_worksheet_isd')
    product2_lpu = fields.Char(
        'Product2 LPU', compute='_compute_worksheet_isd')
    product3_lpu = fields.Char(
        'Product3 LPU', compute='_compute_worksheet_isd')
    product4_lpu = fields.Char(
        'Product4 LPU', compute='_compute_worksheet_isd')
    product5_lpu = fields.Char(
        'Product5 LPU', compute='_compute_worksheet_isd')
    image_teknisi = fields.Binary(
        string="TTD Teknisi", compute='_compute_worksheet_isd')
    image_customer = fields.Binary(
        string="TTD Customer", compute='_compute_worksheet_isd')
    overload = fields.Char(
        string="Overload", compute='_compute_worksheet_isd')
    ptc = fields.Char(
        string="PTC", compute='_compute_worksheet_isd')
    switch = fields.Char(
        string="Switch", compute='_compute_worksheet_isd')
    fan_eva = fields.Char(
        string="Fan Evaporator", compute='_compute_worksheet_isd')
    fan_kon = fields.Char(
        string="Fan Kondensor", compute='_compute_worksheet_isd')
    timer = fields.Char(
        string="Timer", compute='_compute_worksheet_isd')
    lampu = fields.Char(
        string="Lampu TL/FL", compute='_compute_worksheet_isd')
    kondensor = fields.Char(
        string="Kondensor Aux/skin", compute='_compute_worksheet_isd')
    eva = fields.Char(
        string="Evaporator", compute='_compute_worksheet_isd')
    kapiler = fields.Char(
        string="Kapiler", compute='_compute_worksheet_isd')

    cek_filter = fields.Char(
        string="Filter", compute='_compute_worksheet_isd')
    las = fields.Char(
        string="Sambungan Las", compute='_compute_worksheet_isd')
    body_out = fields.Char(
        string="Body Luar", compute='_compute_worksheet_isd')
    body_in = fields.Char(
        string="Body Dalam", compute='_compute_worksheet_isd')
    cek_logo = fields.Char(
        string="Logo", compute='_compute_worksheet_isd')
    pintu = fields.Char(
        string="Pintu/Frame/Kaca", compute='_compute_worksheet_isd')
    karet = fields.Char(
        string="Karet Pintu", compute='_compute_worksheet_isd')
    top_cover = fields.Char(
        string="Top Cover", compute='_compute_worksheet_isd')
    engsel = fields.Char(
        string="Engsel", compute='_compute_worksheet_isd')
    roda = fields.Char(
        string="Roda/Adjuster", compute='_compute_worksheet_isd')
    
    handle = fields.Char(
        string="Handle Pintu", compute='_compute_worksheet_isd')
    kunci = fields.Char(
        string="Kunci", compute='_compute_worksheet_isd')
    grill_on = fields.Char(
        string="Grill Depan", compute='_compute_worksheet_isd')
    grill_off = fields.Char(
        string="Grill Belakang", compute='_compute_worksheet_isd')
    cek_arc = fields.Char(
        string="Arcrilic Advertising", compute='_compute_worksheet_isd')
    cek_cover = fields.Char(
        string="Cover L/R", compute='_compute_worksheet_isd')
    cek_rak = fields.Char(
        string="Rak/Keranjang", compute='_compute_worksheet_isd')
    cek_price = fields.Char(
        string="Price Menu", compute='_compute_worksheet_isd')
    buang_air = fields.Char(
        string="Pembuangan Air", compute='_compute_worksheet_isd')
    cek_isi = fields.Char(
        string="Isi Produk", compute='_compute_worksheet_isd')

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        res = super(ProjectTask, self).search_read(domain, fields, offset, limit, order)

        if self == self.env["project.task"]:
            lstProjectTask = self.env['project.task'].sudo().search(domain)
            for objProjectTask in lstProjectTask:
                for objOtherUser in objProjectTask.otheruser_id:
                    objData = {
                        'id': objProjectTask.id,
                        'display_name': objProjectTask.display_name + '01',
                        'planned_date_begin': objProjectTask.planned_date_begin,
                        'planned_date_end': objProjectTask.planned_date_end,
                        'user_id': [objOtherUser.res_users.id, objOtherUser.res_users.name],
                        'partner_id': [objProjectTask.partner_id.id, objProjectTask.partner_id.name],
                        'planning_overlap': objProjectTask.planning_overlap,
                        'is_fsm': objProjectTask.is_fsm,
                        'project_color': objProjectTask.project_color
                    }
                    if 'worksheet_color' in fields:
                        objData["worksheet_color"] = 8
                    else:
                        objData["project_color"] = 2

                    if fields == ['display_name', 'planned_date_begin', 'planned_date_end', 'user_id', 'partner_id',
                                  'planning_overlap', 'is_fsm', 'project_color', 'worksheet_color'] or fields == [
                        'display_name', 'planned_date_begin', 'planned_date_end', 'user_id', 'partner_id',
                        'planning_overlap', 'is_fsm', 'project_color']:
                        res.append(objData)

                    if fields == ['display_name', 'planned_date_begin', 'planned_date_end', 'project_id', 'user_id',
                                  'partner_id', 'planning_overlap', 'is_fsm', 'project_color'] or fields == [
                        'display_name', 'planned_date_begin', 'planned_date_end', 'project_id', 'user_id',
                        'partner_id', 'planning_overlap', 'is_fsm', 'project_color', 'worksheet_color']:
                        objData["project_id"] = [objProjectTask.project_id.id, objProjectTask.project_id.name]
                        res.append(objData)

                    if fields == ['display_name', 'planned_date_begin', 'planned_date_end', 'worksheet_template_id',
                                  'user_id', 'partner_id', 'planning_overlap', 'is_fsm', 'project_color',
                                  'worksheet_color']:
                        objData["worksheet_template_id"] = [objProjectTask.worksheet_template_id.id, objProjectTask.worksheet_template_id.name]
                        res.append(objData)

        return res

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        res = super(ProjectTask, self).read_group(domain, fields, groupby, offset, limit, orderby, lazy)

        if self == self.env["project.task"]:
            lstProjectTask = self.env['project.task'].sudo().search(domain)

            for objProjectTask in lstProjectTask:
                for objOtherUser in objProjectTask.otheruser_id:
                    for objResult in res:
                        if fields == ['display_name', 'planned_date_begin', 'planned_date_end', 'user_id', 'partner_id',
                            'planning_overlap', 'is_fsm', 'project_color']:
                            if objResult["user_id"][0] == objOtherUser.res_users.id:
                                objResult["user_id_count"] = objResult["user_id_count"] + 1
                            else:
                                objData = {
                                    'user_id_count': 1,
                                    'user_id': [objOtherUser.res_users.id, objOtherUser.res_users.name],
                                    '__domain': objResult["__domain"]
                                }
                                res.append(objData)

                        if fields == ['display_name', 'planned_date_begin', 'planned_date_end', 'project_id',
                                      'user_id', 'partner_id', 'planning_overlap', 'is_fsm', 'project_color'] or fields == [
                            'display_name', 'planned_date_begin', 'planned_date_end', 'project_id',
                            'user_id', 'partner_id', 'planning_overlap', 'is_fsm', 'project_color', 'worksheet_color']:
                            if objResult["project_id"][0] == objProjectTask.project_id.id:
                                if objResult["user_id"][0] == objOtherUser.res_users.id:
                                    objResult["__count"] = objResult["__count"] + 1
                                else:
                                    objData = {
                                        '__count': 1,
                                        'project_id': objResult["project_id"],
                                        'user_id': [objOtherUser.res_users.id, objOtherUser.res_users.name],
                                        '__domain': objResult["__domain"]
                                    }
                                    res.append(objData)

                        if fields == ['display_name', 'planned_date_begin', 'planned_date_end',
                                      'worksheet_template_id', 'user_id', 'partner_id', 'planning_overlap',
                                      'is_fsm', 'project_color', 'worksheet_color']:
                            if objResult["worksheet_template_id"] != False:
                                if objResult["worksheet_template_id"][0] == objProjectTask.worksheet_template_id.id:
                                    if objResult["user_id"][0] == objOtherUser.res_users.id:
                                        objResult["__count"] = objResult["__count"] + 1
                                    else:
                                        objData = {
                                            '__count': 1,
                                            'worksheet_template_id': objResult["worksheet_template_id"],
                                            'user_id': [objOtherUser.res_users.id, objOtherUser.res_users.name],
                                            '__domain': objResult["__domain"]
                                        }
                                        res.append(objData)
                            else:
                                if objProjectTask.worksheet_template_id.id == False:
                                    if objResult["user_id"][0] == objOtherUser.res_users.id:
                                        objResult["__count"] = objResult["__count"] + 1
                                    else:
                                        objData = {
                                            '__count': 1,
                                            'worksheet_template_id': objResult["worksheet_template_id"],
                                            'user_id': [objOtherUser.res_users.id, objOtherUser.res_users.name],
                                            '__domain': objResult["__domain"]
                                        }
                                        res.append(objData)

        return res

    @api.depends('planned_date_begin', 'planned_date_end', 'user_id')
    def _compute_planning_overlap(self):
        if self.ids:
            query = """
                    SELECT T1.id, COUNT(T2.id)
                    FROM
                        (
                        SELECT
                            T.id as id,
                            T.user_id as user_id,
                            T.project_id,
                            T.planned_date_begin as planned_date_begin,
                            T.planned_date_end as planned_date_end,
                            T.active as active
                        FROM project_task T
                        LEFT OUTER JOIN project_project P ON P.id = T.project_id
                        WHERE T.id IN %s
                            AND T.active = 't'
                            AND P.is_fsm = 't'
                            AND T.planned_date_begin IS NOT NULL
                            AND T.planned_date_end IS NOT NULL
                            AND T.project_id IS NOT null
                            
                        union 
                            select pto.task_id as id, pto.res_users as user_id, pt.project_id, pt.planned_date_begin as planned_date_begin,
                            pt.planned_date_end as planned_date_end,
                            pt.active as active
                            from project_task_otheruser pto
                            inner join project_task pt on pt.id = pto.task_id 
                            where pt.id IN %s and pt.active = 't'
                                    AND pt.planned_date_begin IS NOT NULL
                                    AND pt.planned_date_end IS NOT NULL
                                    AND pt.project_id IS NOT null
                        ) T1
                    inner join (
                            select id, user_id, planned_date_begin, planned_date_end, project_id from project_task pt 
                            where pt.active = 't' and pt.planned_date_begin IS NOT NULL AND pt.planned_date_end IS NOT NULL AND pt.project_id IS NOT null
                            
                            union
                            select pto.task_id as id, pto.res_users as user_id,  
                                pt.planned_date_begin as planned_date_begin, pt.planned_date_end as planned_date_end,
                                pt.project_id
                            from project_task_otheruser pto
                            inner join project_task pt on pt.id = pto.task_id 
                            where pt.active = 't' AND pt.planned_date_begin IS NOT NULL AND pt.planned_date_end IS NOT null AND pt.project_id IS NOT NULL
                        ) T2
                        ON T1.id != T2.id AND T1.user_id = T2.user_id
                            AND (T1.planned_date_begin::TIMESTAMP, T1.planned_date_end::TIMESTAMP)
                                OVERLAPS (T2.planned_date_begin::TIMESTAMP, T2.planned_date_end::TIMESTAMP)
                    GROUP BY T1.id
                """
            self.env.cr.execute(query, (tuple(self.ids), tuple(self.ids),))
            raw_data = self.env.cr.dictfetchall()
            overlap_mapping = dict(map(lambda d: d.values(), raw_data))
            for task in self:
                task.planning_overlap = overlap_mapping.get(task.id, 0)
        else:
            self.planning_overlap = False


    def _compute_worksheet_isd(self):
        #self.worksheet_template_id
        #self.worksheet_template_id.model_id.model
        asd = ''

        objWorkSheet = self.env[self.worksheet_template_id.model_id.model].sudo().search(
            [("x_task_id", "=", self.id)], limit=1)

        dblPrice = 0

        #report LPU
        ojbNama = ''
        ojbAlamat = ''
        objKota = ''
        objZipcode = ''
        objCode = ''
        objMerk = ''
        objType = ''
        objLogo = ''
        objModel = ''
        objSerial = ''
        objKategori = ''
        objDateLpu = ''
        objCeklistrik = ''
        objCekTegangan = ''
        objCekKabel = ''
        objCekWiring = ''
        objCekKapasitor = ''
        objCekKompressor = ''
        objCekThermostat = ''
        objCekBallast = ''
        objCekRelay = ''
        objCekBungaEs = ''
        objNoreges = ''
        objNoregesganti = ''
        objFotoUnit = ''
        objKerusakan = ''
        objHasilAnalisa = ''
        objHasilAkhir = ''
        objProduct1 = ''
        objProduct2 = ''
        objProduct3 = ''
        objProduct4 = ''
        objProduct5 = ''
        objttdTeknisi = ''
        objttdCustomer = ''
        objCekOver = ''
        objCekPTC = ''
        objCekSwitch = ''
        objCekFaneva = ''
        objCekFankon = ''
        objCekTimer = ''
        objCekLampu = ''
        objCekKondensor = ''
        objCekEva = ''
        objCekKap = ''
        objCekFilter = ''
        objCekLas = ''
        objCekBodyout = ''
        objCekBodyin = ''
        objCekLogo = ''
        objCekPintu = ''
        objCekKaret = ''
        objCekTop = ''
        objCekEngsel = ''
        objCekRoda = ''
        objCekHandle = ''
        objCekKunci = ''
        objCekGrillon = ''
        objCekGrilloff = ''
        objCekArcrilic = ''
        objCekCover = ''
        objCekRak = ''
        objCekPrice = ''
        objCekBuangAir = ''
        objCekIsi = ''

        for objField in self.worksheet_template_id.model_id.field_id:
            if objField.relation == "product.product":
                objProduct = objWorkSheet[objField.name]
                dblPrice = dblPrice + objProduct.list_price
            
            if objField.relation == "project.task":
                objUnit = objWorkSheet[objField.name]
                ojbNama = objUnit.default_code.location
                ojbAlamat = objUnit.default_code.alamat
                objKota = objUnit.default_code.city.display_name
                objZipcode = objUnit.default_code.kode_pos
                objCode = objUnit.default_code.description
                objMerk = objUnit.default_code.merk
                objType = objUnit.default_code.unit_type.display_name
                objLogo = objUnit.default_code.logo
                objModel = objUnit.default_code.model
                objSerial = objUnit.default_code.serial
                # objKategori = objUnit.default_code.unit_categ
        
        for objData in objWorkSheet:
            objDateLpu = objData.x_studio_tanggal_
            objKategori = objData.x_studio_kategori_unit_
            objCeklistrik = objData.x_studio_sumber_listrik
            objCekTegangan = objData.x_studio_tegangan
            objCekKabel = objData.x_studio_kabel_power
            objCekWiring = objData.x_studio_wiring
            objCekKapasitor = objData.x_studio_kapasitor
            objCekKompressor = objData.x_studio_kompressor_1
            objCekThermostat = objData.x_studio_thermostat_1
            objCekBallast = objData.x_studio_ballast
            objCekRelay = objData.x_studio_relay_1
            objCekBungaEs = objData.x_studio_bunga_es
            objNoreges = objData.x_studio_no_registrasi_
            objNoregesganti = objData.x_studio_no_registrasi_pengganti_
            objFotoUnit = objData.x_studio_foto_unit_1
            objKerusakan = objData.x_studio_kerusakan
            objHasilAnalisa = objData.x_studio_hasil_akhir_analisa_
            objHasilAkhir = objData.x_studio_hasil_akhir_keterangan_
            objProduct1 = objData.x_studio_1_.display_name
            objProduct2 = objData.x_studio_2_.display_name
            objProduct3 = objData.x_studio_3_.display_name
            objProduct4 = objData.x_studio_4_.display_name
            objProduct5 = objData.x_studio_5_.display_name
            objttdTeknisi = objData.x_studio_teknisi
            objttdCustomer = objData.x_studio_customer_1
            objCekOver = objData.x_studio_overload
            objCekPTC = objData.x_studio_ptc
            objCekSwitch = objData.x_studio_switch
            objCekFaneva = objData.x_studio_fan_evaporator
            objCekFankon = objData.x_studio_fan_kondensor
            objCekTimer = objData.x_studio_timer
            objCekLampu = objData.x_studio_lampu_tl_fl
            objCekKondensor = objData.x_studio_kondensor_aux_skin
            objCekEva = objData.x_studio_evaporator
            objCekKap = objData.x_studio_kapiler
            objCekFilter = objData.x_studio_filter
            objCekLas = objData.x_studio_sambungan_las
            objCekBodyout = objData.x_studio_body_luar
            objCekBodyin = objData.x_studio_body_dalam
            objCekLogo = objData.x_studio_logo
            objCekPintu = objData.x_studio_pintu_frame_kaca
            objCekKaret = objData.x_studio_karet_pintu
            objCekTop = objData.x_studio_top_cover
            objCekEngsel = objData.x_studio_engsel_1
            objCekRoda = objData.x_studio_roda_adjuster
            objCekHandle = objData.x_studio_handle_pintu
            objCekKunci = objData.x_studio_kunci
            objCekGrillon = objData.x_studio_grill_depan
            objCekGrilloff = objData.x_studio_grill_belakang
            objCekArcrilic = objData.x_studio_acrillic_advertising
            objCekCover = objData.x_studio_cover_lr
            objCekRak = objData.x_studio_rak_keranjang
            objCekPrice = objData.x_studio_price_menu
            objCekBuangAir = objData.x_studio_pembuangan_air
            objCekIsi = objData.x_studio_isi_produk

        self.total_worksheet_product = dblPrice
        self.nama_lpu = ojbNama
        self.alamat_lpu = ojbAlamat
        self.kota_lpu = objKota
        self.zipcode_lpu = objZipcode
        self.code_lpu = objCode
        self.merk_lpu = objMerk
        self.type_lpu = objType
        self.logo_lpu = objLogo
        self.model_lpu = objModel
        self.serial_lpu = objSerial
        self.kategori_lpu = objKategori
        self.tanggal_lpu = objDateLpu
        self.listrik_lpu = objCeklistrik
        self.tegangan_lpu = objCekTegangan
        self.kabel_lpu = objCekKabel
        self.wiring_lpu = objCekWiring
        self.kapasitor_lpu = objCekKapasitor
        self.kompresor_lpu = objCekKompressor
        self.thermostat_lpu = objCekThermostat
        self.ballast_lpu = objCekBallast
        self.relay_lpu = objCekRelay
        self.bunga_lpu = objCekBungaEs
        self.noreges_lpu = objNoreges
        self.noreges_ganti_lpu = objNoregesganti
        self.image_unit = objFotoUnit
        self.image_rusak = objKerusakan
        self.analisa_lpu = objHasilAnalisa
        self.akhir_lpu = objHasilAkhir
        self.product1_lpu = objProduct1
        self.product2_lpu = objProduct2
        self.product3_lpu = objProduct3
        self.product4_lpu = objProduct4
        self.product5_lpu = objProduct5
        self.image_teknisi = objttdTeknisi
        self.image_customer = objttdCustomer
        self.overload = objCekOver
        self.ptc = objCekPTC
        self.switch = objCekSwitch
        self.fan_eva = objCekFaneva
        self.fan_kon = objCekFankon
        self.timer = objCekTimer
        self.lampu = objCekLampu
        self.kondensor = objCekKondensor
        self.eva = objCekEva
        self.kapiler = objCekKap

        self.cek_filter = objCekFilter
        self.las = objCekLas
        self.body_out = objCekBodyout
        self.body_in = objCekBodyin
        self.cek_logo = objCekLogo
        self.pintu = objCekPintu
        self.karet = objCekKaret
        self.top_cover = objCekTop
        self.engsel = objCekEngsel
        self.roda = objCekRoda

        self.handle = objCekHandle
        self.kunci = objCekKunci
        self.grill_on = objCekGrillon
        self.grill_off = objCekGrilloff
        self.cek_arc = objCekArcrilic
        self.cek_cover = objCekCover
        self.cek_rak = objCekRak
        self.cek_price = objCekPrice
        self.buang_air = objCekBuangAir
        self.cek_isi = objCekIsi
       

    def btnCallUnit(self):
        context = dict(self.env.context)
        return {
            'name': 'Unit Product',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'product.unit',
            'res_id': self.default_code.id,
            'type': 'ir.actions.act_window',
            'target': 'current',
            'nodestroy': True,
            'context': context,
        }

    def btnCallSupervisor(self):
        if self.helpdesk_ticket_id.team_id.leader_user_id.mobile:
            return {
                'name': 'Go to website',
                'res_model': 'ir.actions.act_url',
                'type': 'ir.actions.act_url',
                'target': 'new',
                'url': "https://wa.me/" + self.helpdesk_ticket_id.team_id.leader_user_id.mobile + "?text=hahahaha"
            }

    def btnOnHold(self):
        self.user_checking.unlink()
        self.env['project.task.checkinguser'].sudo().create({ 'task_id': self.id, 'res_users': self.user_id.id, 'sts_typeuser': '1' })
        for objOther in self.otheruser_id:
            self.env['project.task.checkinguser'].sudo().create({ 'task_id': self.id, 'res_users': objOther.res_users.id })

        self.stsonhold = '1'
        if self.timer_start:
            self.action_timer_pause()

    def _fsm_create_sale_order(self):
        res = super(ProjectTask, self)._fsm_create_sale_order()
        if self.default_code.owner.id:
            if date.today() <= self.default_code.tgl_exp:
                self.sale_order_id.partner_id = self.default_code.owner.id
                self.sale_order_id.partner_invoice_id = self.default_code.owner.id
                self.sale_order_id.partner_shipping_id = self.default_code.owner.id


    def _fsm_create_sale_order_line(self):
        deltaFrom = fields.Datetime.now()
        deltaTo = fields.Datetime.now()
        intDays = 1

        if len(self.timesheet_ids) > 0:
            for objTimesheet in self.timesheet_ids:
                if deltaFrom > objTimesheet.create_date: deltaFrom = objTimesheet.create_date
                if deltaTo < objTimesheet.create_date: deltaTo = objTimesheet.create_date
            delta = deltaTo - deltaFrom
            intDays = delta.days + 1

        domain = [("type", "=", "service"), ("invoice_policy", "=", "delivery"),
                  ("service_type", "=", "timesheet"),
                  ("isd_total_work_hour", "<=", intDays * 24),
                  ("sts_service_unit", "=", self.default_code.unit_categ)]
        objProductService = self.env['product.template'].sudo().search(domain, limit=1,
                                                                       order="isd_total_work_hour desc")
        if objProductService.id:
            if not self.sale_order_id:
                self._fsm_ensure_sale_order()

            if objProductService.product_variant_id.id != self.sale_line_id.product_id.id:
                self.timesheet_product_id = objProductService.product_variant_id.id
                self.sale_line_id.unlink()

                sale_order_line = self.env['sale.order.line'].sudo().create({
                    'order_id': self.sale_order_id.id,
                    'product_id': self.timesheet_product_id.id,
                    'project_id': self.project_id.id,
                    'task_id': self.id,
                    'product_uom_qty': 1,
                    'qty_delivered': 1,
                    'product_uom': self.project_id.timesheet_product_id.uom_id.id,
                })
                self.write({
                    'sale_line_id': sale_order_line.id,
                })

                # assign SOL to timesheets
                self.env['account.analytic.line'].sudo().search([
                    ('task_id', '=', self.id),
                    ('so_line', '=', False),
                    ('project_id', '!=', False)
                ]).write({
                    'so_line': sale_order_line.id
                })

    def action_fsm_validate(self):
        self._fsm_create_sale_order_line()

        if len(self.user_checking) == 0:
            self.user_checking.unlink()
            self.env['project.task.checkinguser'].sudo().create({'task_id': self.id, 'res_users': self.user_id.id, 'sts_typeuser': '1'})
            for objOther in self.otheruser_id:
                self.env['project.task.checkinguser'].sudo().create({'task_id': self.id, 'res_users': objOther.res_users.id})

        self.user_fixing.unlink()
        self.env['project.task.fixinguser'].sudo().create({'task_id': self.id, 'res_users': self.user_id.id, 'sts_typeuser': '1'})
        for objOther in self.otheruser_id:
            self.env['project.task.fixinguser'].sudo().create({'task_id': self.id, 'res_users': objOther.res_users.id})

        self.stsonhold = '2'
        res = super().action_fsm_validate()
        self.sale_line_id.qty_delivered = 1

        return res

    @api.model
    def create(self, vals):
        if vals.get('name_seq_fs', _('New')) == _('New'):
            vals['name_seq_fs'] = self.env['ir.sequence'].next_by_code('project.task.sequence') or _('New')

        if vals.get('task_no', _('New')) == _('New'):
            vals['task_no'] = self.env['ir.sequence'].next_by_code('project.task.number') or _('New')

        result = super(ProjectTask, self).create(vals)
        return result
    


class res_users(models.Model):
    _name = 'project.task.otheruser'

    task_id = fields.Many2one('project.task')
    res_users = fields.Many2one('res.users', string='Assigned to')

class checkingusers(models.Model):
    _name = 'project.task.checkinguser'

    name = fields.Char(string='Checking User', related='res_users.name')
    task_id = fields.Many2one('project.task')
    res_users = fields.Many2one('res.users', string='Assigned to')
    sts_typeuser = fields.Selection([
        ('0', 'Assistant'),
        ('1', 'Leader')
    ], string="Team Status", default="0", required=True)

class fixingusers(models.Model):
    _name = 'project.task.fixinguser'

    name = fields.Char(string='Checking User', related='res_users.name')
    task_id = fields.Many2one('project.task')
    res_users = fields.Many2one('res.users', string='Assigned to')
    sts_typeuser = fields.Selection([
        ('0', 'Assistant'),
        ('1', 'Leader')
    ], string="Team Status", default="0", required=True)