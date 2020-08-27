from library import app
from flask import jsonify, request, make_response
import json

from library.BLL import BorrowTicketSvc
from library.Common.Req.BorrowTicketReq import CreateBorrowTicketReq, UpdateBorrowTicketReq, DeleteBorrowTicketReq, \
    SearchBorrowTicketReq
from library.Common.Req.GetItemsByPageReq import GetItemsByPageReq
from library.Common.Rsp.BorrowTicketRsp import SearchBorrowTicketRsp
from library.Common.Rsp.GetImtesByPageRsp import GetItemsByPageRsp
from library.Common.Rsp.SingleRsp import ErrorRsp


@app.route('/admin/borrow-ticket-management/get-borrow-tickets', methods=['POST', 'GET'])
def GetBorrowTickets():
    req = GetItemsByPageReq(request.json)
    result = BorrowTicketSvc.GetBorrowTicketsByPage(req)
    res = GetItemsByPageRsp(has_next=result['has_next'], has_prev=result['has_prev'],
                            items=result['borrow_tickets']).serialize()
    return jsonify(res)


@app.route('/admin/borrow-ticket-management/create-borrow-ticket', methods=['POST', 'GET'])
def CreateBorrowTicket():
    req = CreateBorrowTicketReq(request.json)
    result = BorrowTicketSvc.CreateBorrowTicket(req)
    return jsonify(result)


@app.route('/admin/borrow-ticket-management/update-borrow-ticket', methods=['POST', 'GET'])
def UpdateBorrowTicket():
    req = UpdateBorrowTicketReq(request.json)
    result = BorrowTicketSvc.UpdateBorrowTciket(req)
    return jsonify(result)


@app.route('/admin/borrow-ticket-management/delete-borrow-ticket', methods=['POST', 'GET'])
def DeleteBorrowTicket():
    req = DeleteBorrowTicketReq(request.json)
    result = BorrowTicketSvc.DeleteBorrowTicket(req)
    return jsonify(result)


@app.route('/admin/borrow-ticket-management/search-borrow-ticket', methods=['POST', 'GET'])
def SearchBorrowTicket():
    req = SearchBorrowTicketReq(request.json)
    result = BorrowTicketSvc.SearchBorrowTicket(req)
    res = SearchBorrowTicketRsp(result).serialize()
    return jsonify(res['borrowtickets'])