from sqlalchemy import or_

from library import db
from library.Common.Req.OrderDetailReq import CreateOrderDetailReq
from library.DAL import models
from flask import jsonify, json
from library.Common.util import ConvertModelListToDictList
from library.Common.Req import GetItemsByPageReq
from datetime import datetime


def GetOrderDetailsByPage(req: GetItemsByPageReq):
    order_detail_pagination = models.Orderdetails.query.paginate(per_page=req.per_page, page=req.page)
    has_next = order_detail_pagination.has_next
    has_prev = order_detail_pagination.has_prev
    order_details = ConvertModelListToDictList(order_detail_pagination.items)
    return has_next, has_prev, order_details


def CreateOrderDetail(req: CreateOrderDetailReq):
    create_order_detail = models.Orderdetails(order_id=req.order_id,
                                              book_id=req.book_id,
                                              retail_price=req.retail_price,
                                              quantity=req.quantity,
                                              discount=req.discount,
                                              total=req.total,
                                              note=req.note,
                                              delete_at=req.delete_at)

    db.session.add(create_order_detail)
    db.session.commit()
    return create_order_detail.serialize()