import csv
from io import StringIO

from flask import Blueprint, request, abort, make_response
from flask_restful import Api
from flasgger import swag_from

from app.views import BaseResource, check_auth

from app.models import db
from app.models.user_models import UserModel, InfoModel, ApplyStatusModel, AdmissionChoice

from app.docs.search import VIEW_APPLICANTS_GET

api = Api(Blueprint(__name__, __name__))


@api.resource('/applicants')
class ViewApplicants(BaseResource):
    @swag_from(VIEW_APPLICANTS_GET)
    @check_auth()
    def get(self):
        search_name = request.args.get('name', default='')
        search_region = request.args.get('region', default='')
        search_admission = request.args.get('admission', default='')
        checking_receipt = request.args.get('receipt', default=False)
        checking_payment = request.args.get('payment', default=False)

        joined_res = db.session.query(UserModel, InfoModel, ApplyStatusModel) \
            .join(InfoModel) \
            .join(ApplyStatusModel) \
            .join(ApplyStatusModel.final_submit is True)

        # 제출-전형료 조건 없음
        if not (checking_receipt and checking_payment):
            filtered_res = joined_res

        # 제출-전형료 조건 있음
        else:
            filtered_res = joined_res \
                .filter(ApplyStatusModel.receipt == self.str_to_bool(checking_receipt)) \
                .filter(ApplyStatusModel.payment == self.str_to_bool(checking_payment))

        if search_name:
            filtered_res = filtered_res.filter(InfoModel.name.like('%' + search_name + '%')).all()
        if search_admission:
            filtered_res = filtered_res.filter(UserModel.admission == AdmissionChoice(int(search_admission))).all()
        if search_region:
            filtered_res = filtered_res.filter(UserModel.region == self.str_to_bool(search_region)).all()

        return self.unicode_safe_json_dumps([{
            'user_id': student.UserModel.user_id,
            'receipt_code': student.ApplyStatusModel.receipt_code,
            'name': student.InfoModel.name,
            'region': '대전' if student.UserModel.region is True else '전국',
            'admission': student.UserModel.admission.name,
            'receipt': student.ApplyStatusModel.receipt,
            'payment': student.ApplyStatusModel.payment
        } for student in filtered_res], 200)


@api.resource('/applicants/excel')
class PrintExcelAllApplicants(BaseResource):
    @swag_from()
    @check_auth()
    def post(self):
        pass
#         search_res = request.json
#         si = StringIO()
#         si.write(u'\ufeff')
#         f = csv.writer(si)
#
#         f.writerow(["receipt_code", "name", "region", "type", "receipt", "payment"])
#         for r in search_res:
#             f.writerow([r["receipt_code"], r["name"], r["region"], r["type"], r["receipt"], r["payment"]])
#
#         res = make_response(si.getvalue(), 201)
#         res.headers['Content-Disposition'] = "attachment; filename=applicants.csv"
#         res.headers['Content-type'] = "text/csv"
#
#         return res


@api.resource('/applicants/exam_table')
class PrintExamTableAllApplicants(BaseResource):
    @swag_from()
    @check_auth()
    def post(self):
        pass
