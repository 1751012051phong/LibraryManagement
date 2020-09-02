from sqlalchemy import or_

from library import db
from library.Common.Req import GetItemsByPageReq
from library.Common.Req.OrderReq import CreateOrderReq, UpdateOrderReq, DeleteOrderReq, SearchOrdersReq
from library.Common.Rsp.OrderRsp import SearchOrdersRsp
from library.Common.Rsp.SingleRsp import ErrorRsp
from library.Common.util import ConvertModelListToDictList
from library.DAL import models
from flask import jsonify, json

from datetime import datetime


def GetOrdersbyPage(req: GetItemsByPageReq):
    orders_pagination = models.Orders.query.filter(models.Orders.delete_at == None).paginate(per_page=req.per_page,
                                                                                             page=req.page)
    has_next = orders_pagination.has_next
    has_prev = orders_pagination.has_prev
    employees = ConvertModelListToDictList(orders_pagination.items)
    return has_next, has_prev, employees


def CreateOrder(order: CreateOrderReq):
    create_order = models.Orders(customer_id=order.customer_id,
                                 employee_id=order.employee_id,
                                 order_date=order.order_date,
                                 type=order.type,
                                 total=order.total,
                                 note=order.note,
                                 delete_at=order.delete_at)

    db.session.add(create_order)
    db.session.commit()

    for order_detail in order.order_detail_list:
        order_book = models.Books.query.get(order_detail['book_id'])
        order_book.new_amount -= order_detail['quantity']
        if order_book.new_amount < 0:
            raise ErrorRsp(code=400, message='Số lượng sách tồn kho đã hết.')
        new_order_detail = models.Orderdetails(order_id=create_order.serialize()['order_id'],
                                               book_id=order_detail['book_id'],
                                               retail_price=order_book.serialize()['retail_price'],
                                               discount=order_book.serialize()['discount'],
                                               total=(1 - order_book.serialize()['discount']) * (
                                                       order_book.serialize()['retail_price'] * order_detail[
                                                   'quantity']), quantity=order_detail['quantity'])
        create_order.orderdetails.append(new_order_detail)

    db.session.commit()
    return create_order.serialize()


def UpdateOrder(req: UpdateOrderReq):
    update_order = models.Orders.query.get(req.order_id)
    update_order.customer_id = req.customer_id
    update_order.employee_id = req.employee_id
    update_order.order_date = req.order_date
    update_order.type = req.type
    update_order.total = req.total
    update_order.note = req.note
    update_order.delete_at = req.delete_at
    db.session.commit()
    return update_order.serialize()


def DeleteOrder(req: DeleteOrderReq):
    delete_order = models.Orders.query.get(req.order_id)
    delete_order.delete_at = datetime.now()
    db.session.add(delete_order)
    db.session.commit()

    return delete_order.serialize()


def SearchOrders(req: SearchOrdersReq):
    search_order = models.Orders.query.filter(or_(models.Orders.customer_id == req.customer_id,
                                                  models.Orders.order_id == req.order_id,
                                                  models.Orders.employee_id == req.employee_id,
                                                  models.Orders.order_date == req.order_date)).all()
    orders = ConvertModelListToDictList(search_order)
    res = SearchOrdersRsp(orders).serialize()
    return res
