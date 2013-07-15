 # Create your views here.
from django.shortcuts import render_to_response
from models import *
from django.db.models import Q
from django.http import HttpResponseRedirect
from addTraderForm import *
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import datetime

def home(request):
    return render_to_response("login.html",locals())

@csrf_exempt
def login(request):
    error = False
    if 'dealerIDInput' in request.POST and request.POST['dealerIDInput']:
        dID = request.POST["dealerIDInput"]
        dealers = dealer.objects.filter(dID = dID)
        if len(dealers) == 1:
            password = request.POST["passwordInput"]
            if password == dealers[0].password:
                request.session["dName"] = dealers[0].dName
                request.session["dID"] = dealers[0].dID
                return render_to_response("loginSucceed.html",locals())
            else:
                error = "wrong password"
                return render_to_response("error.html",{"error":error})
        else:
            error = "wrong dealer"
            return render_to_response("error.html",{"error":error})

    else:
        return HttpResponse('Please submit a dealerID')

def register(request):
    return render_to_response("register.html",locals())


@csrf_exempt
def regist(request):    
    error = False
    dID = request.POST["dID"]
    dealers = dealer.objects.filter(dID = dID)
    if len(dealers) == 0:
        dName = request.POST["dName"]
        password = request.POST["password"]
        contractInformation = request.POST["contractInformation"]
        if password == request.POST["ConfirmPassword"]:
            new_dealer = dealer(dID = dID,
                                dName = dName,
                                password = password,
                                contractInformation = contractInformation)
            new_dealer.save()
            request.session["dID"] = request.POST["dID"]
            request.session["dName"] = request.POST["dName"]
            return HttpResponseRedirect('/')
        else:
            error = "two different password"
            return render_to_response("error.html",{"error":error})
    else:
        error = "same ID"
        return render_to_response("error.html",{"error":error})

def index(request):
	trans = transationRecord.objects.filter(tdealer=request.session["dName"])
	#if request.GET['tID'] and request.GET.['tAccount'] and request.GET['tdate']:
	#	tid = request.GET['tID']
	#	tac = request.GET['tAccount']
	#	tda = request.GET['tdate']
	#	recs = transationRecord.object.filter(tID=tid)
	return render_to_response('index.html',locals())
 	#return render_to_response('index.html',{'transationRecord.number':1})

def search(request):
	if request.GET['tID']:
		tid = request.GET['tID']
		recs = transationRecord.objects.filter(tID=tid)
	if request.GET['tAccount']:
		tac = request.GET['tAccount']
		recs = transationRecord.objects.filter(tAccount=tac)
		#tac = request.GET['tAccount']
		#tda = request.GET['tdate']
		#recs = transationRecord.objects.filter(tID=tid)
	if request.GET['tdate']:
		tda = request.GET['tdate']
		recs = transationRecord.objects.filter(tdate=tda)
	if request.GET['tID'] and request.GET['tAccount']:
		tid = request.GET['tID']
		tac = request.GET['tAccount']
		recs = transationRecord.objects.filter(tID=tid).filter(tAccount=tac)
	if request.GET['tID'] and request.GET['tdate']:
		tid = request.GET['tID']
		tda = request.GET['tdate']
		recs = transationRecord.objects.filter(tID=tid).filter(tdate=tda)
	if request.GET['tAccount'] and request.GET['tdate']:
		tac = request.GET['tAccount']
		tda = request.GET['tdate']
		recs = transationRecord.objects.filter(tAccount=tac).filter(tdate=tda)
	if request.GET['tID'] and request.GET['tAccount'] and request.GET['tdate']:
		tid = request.GET['tID']
		tac = request.GET['tAccount']
		tda = request.GET['tdate']
		recs = transationRecord.objects.filter(tID=tid).filter(tAccount=tac).filter(tdate=tda)
	return render_to_response('search.html',locals())

def addTrades(request):
	#if request.method == 'GET':
	#	form = addTraderForm(request.POST)
	#	if form.is_valid():
	#		tID = form.clean_data['tID']
	#		tAccount = form.clean_data['tAccount']
	#		consignmentNo = form.clean_data['consignmentNo']
	#		transactionNo = form.clean_data['transactionNo']
	#		transationAmount = form.clean_data['transationAmount']
	#		transationPrice = form.clean_data['transationPrice']
	#		tdate = form.clean_data['tdate']
	#		customerNumber = form.clean_data['customerNumber']
	#else:
	#	form = addTraderForm()
	#return render_to_response('addTrades.html',{"form":form})
	if request.GET['tID'] and request.GET['tAccount'] and request.GET['consignmentNo'] and request.GET['transactionNo'] and request.GET['transationAmount'] and request.GET['transationPrice'] and request.GET['tdate'] and request.GET['customerNumber']:
		tid = request.GET['tID']
		tac = request.GET['tAccount']
		con = request.GET['consignmentNo']
		tra = request.GET['transactionNo']
		tam = request.GET['transationAmount']
		tpr = request.GET['transationPrice']
		tda = request.GET['tdate']
		cus = request.GET['customerNumber']
		rec = transationRecord(tdealer=request.session["dName"],tState='False',tID=tid, tAccount=tac, consignmentNo=con, transactionNo=tra, transationAmount=tam, transationPrice=tpr, tdate=tda, customerNumber=cus)
		rec.save()
		request.session['tID'] = request.GET['tID']
		recs = transationRecord.objects.filter(consignmentNo=con).filter(transactionNo=tra)
		return render_to_response('test.html',locals())

def getTradesTable(request):
	return render_to_response('addTrades.html',locals())

def editPage(request, tid_from_url):
	trans = transationRecord.objects.get(id=tid_from_url)
	return render_to_response('editPage.html',locals())

def DeletePage(request,Delid_from_url):
	trans = transationRecord.objects.get(id=Delid_from_url)
	return render_to_response('DeletePage.html',locals())

def DeleteSave(request,DeleteSaveid_from_url):
	rec = transationRecord(id=DeleteSaveid_from_url)
	rec.delete()
	return HttpResponseRedirect('/index/')

def editSave(request,saveid_from_url):
	if request.GET['tID'] and request.GET['tAccount'] and request.GET['consignmentNo'] and request.GET['transactionNo'] and request.GET['transationAmount'] and request.GET['transationPrice'] and request.GET['tdate'] and request.GET['customerNumber']:
		tid = request.GET['tID']
		tac = request.GET['tAccount']
		con = request.GET['consignmentNo']
		tra = request.GET['transactionNo']
		tam = request.GET['transationAmount']
		tpr = request.GET['transationPrice']
		tda = request.GET['tdate']
		cus = request.GET['customerNumber']
		rec = transationRecord(id=saveid_from_url,tdealer=request.session["dName"],tState='False',tID=tid, tAccount=tac, consignmentNo=con, transactionNo=tra, transationAmount=tam, transationPrice=tpr, tdate=tda, customerNumber=cus)
		rec.save()
		return HttpResponseRedirect('/index/')

def AllocatePage(request,Allocateid_from_url):
	trans = transationRecord.objects.get(id=Allocateid_from_url)
	cus = customerAccount.objects.filter(consignmentNo=trans.consignmentNo)
	return render_to_response('AllocatePage.html',locals())

def AllocateResult(request,Resultid_from_url):
	return render_to_response('AllocateResult.html',locals())

def Result(request,resultid_from_url):
	trans = transationRecord.objects.get(id=Resultid_from_url)
	consignmentNo = trans[0].consignmentNo
	tID = trans[0].tID
	

def propertyInfo(request,tID_from_url):
	ass = assetInformation.objects.get(tID=tID_from_url)
	return render_to_response('propertyInfo.html',locals())

def Allocate(request,allocateid_from_url):
	return render_to_response('Allocate.html',locals())
	

