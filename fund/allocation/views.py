 # Create your views here.
from django.shortcuts import render_to_response
from models import *
from django.db.models import Q
from django.http import HttpResponseRedirect
from addTraderForm import *
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import itertools
import datetime

from mmap import mmap,ACCESS_READ
from xlrd import open_workbook

def read(request):
    wb = open_workbook('records.xls')

    for s in wb.sheets():
        for row in range(s.nrows):
            if len(transationRecord.objects.filter(consignmentNo = s.cell(row,4).value)) < 1:
                new_transationRecord = transationRecord(
                    tdealer = s.cell(row,0).value,
                    tState = s.cell(row,1).value,
                    tID = s.cell(row,2).value,
                    tAccount = s.cell(row,3).value,
                    consignmentNo = s.cell(row,4).value,
                    transactionNo = s.cell(row,5).value,
                    transationAmount = s.cell(row,6).value,
                    transationPrice = s.cell(row,7).value,
                    tdate = s.cell(row,8).value,
                    customerNumber = s.cell(row,9).value,
                    )
                new_transationRecord.save()
    return HttpResponseRedirect('/index/')


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

@csrf_exempt
def supervisorLogin(request):
    error = False
    if 'supervisorIDInput' in request.POST and request.POST['supervisorIDInput']:
        sID = request.POST["supervisorIDInput"]
        supervisors = supervisor.objects.filter(sID = sID)
        if len(supervisors) == 1:
            password = request.POST["supervisorpasswordInput"]
            if password == supervisors[0].password:
                request.session["sName"] = supervisors[0].sName
                request.session["sID"] = supervisors[0].sID
                return render_to_response("supervisorloginSucceed.html",locals())
            else:
                error = "wrong password"
                return render_to_response("error.html",{"error":error})
        else:
            error = "wrong supervisor"
            return render_to_response("error.html",{"error":error})

    else:
        return HttpResponse('Please submit a dealerID')

def register(request):
    return render_to_response("register.html",locals())

def supervisorRegister(request):
	return render_to_response('supervisorRegister.html',locals())

 
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

@csrf_exempt
def supervisorRegist(request):    
    error = False
    sID = request.POST["sID"]
    supervisors = supervisor.objects.filter(sID = sID)
    if len(supervisors) == 0:
        sName = request.POST["sName"]
        password = request.POST["password"]
        contractInformation = request.POST["scontractInformation"]
        if password == request.POST["ConfirmPassword"]:
            new_supervisor = supervisor(sID = sID,
                                sName = sName,
                                password = password,
                                contractInformation = contractInformation)
            new_supervisor.save()
            request.session["sID"] = request.POST["sID"]
            request.session["sName"] = request.POST["sName"]
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

def supervisorIndex(request):
	trans = transationRecord.objects.filter(tState='True')
	return render_to_response('supervisorIndex.html',locals())

def supervisorCheckPage(request,supervisorcheckid_from_url):
	trans = transationRecord.objects.get(id=supervisorcheckid_from_url)
	return render_to_response('supervisorCheckPage.html',locals())

def saveResult(request,saveResultid_from_url):
	temp = request.GET['consignmentNo']
	checkRe = checkResult.objects.filter(consignmentNo=temp)
	if len(checkRe)==0:
		if request.GET['consignmentNo'] and request.GET['is_pass'] and request.GET['reason']:
			con = request.GET['consignmentNo']
			isp = request.GET['is_pass']
			res = request.GET['reason']
			checkr = checkResult(consignmentNo=con,sName=request.session["sName"],is_pass=isp,checkInformation=res)
			checkr.save()
	tra = transationRecord.objects.get(id=saveResultid_from_url)
	tid = tra.id
	tdealer = tra.tdealer
	tID = tra.tID
	tAccount = tra.tAccount
	transactionNo = tra.transactionNo
	transationAmount = tra.transationAmount
	transationPrice = tra.transationPrice
	tdate = tra.tdate
	customerNumber = tra.customerNumber
	transa = transationRecord(id=tid,tdealer=tdealer,tState='Pass',tID=tID,tAccount=tAccount,consignmentNo=con,transactionNo=transactionNo,transationAmount=transationAmount,transationPrice=transationPrice,tdate=tdate,customerNumber=customerNumber)
	transa.save()
	return HttpResponseRedirect('/index')

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
	trans = transationRecord.objects.get(id=Resultid_from_url)
	cus = customerAccount.objects.filter(consignmentNo=trans.consignmentNo)
	extra_condition = request.GET.get('extra_condition','')
	results = {
		'Single':lambda: single_allocate(cus),
		'Waterfall':lambda: waterfall_allocate(cus),
		}[extra_condition]()
	return render_to_response('AllocateResult.html',locals())
	
def single_allocate(cus):
	results = []
	con = cus[0].consignmentNo
	tra = transationRecord.objects.get(consignmentNo=con)
	amount = tra.transationAmount
	customer = customerAccount.objects.get(consignmentNo=con)
	cid = customer.cID
	fil = result.objects.filter(consignmentNo=con)
	if len(fil)==0:	
		rec = result(consignmentNo=con,cID=cid,allocationInformation=amount)
		rec.save()
	results = result.objects.filter(consignmentNo=con)
	return results


def waterfall_allocate(cus):
	results = []
	resc = []
	temp = []
	cid = []
	exist = []
	targetweighting = []
	distribute = []
	holding = []
	total = []
	priority = []
	designatedQuantity = []
	
	#results = sorted(cus,key = lambda x:x[10],reverse = False)
	for c in cus:
		a = (c.cID, c.consignmentNo, c.ExistingPercentage,c.priority, c.designatedQuantity)
		temp.append(a)
	
	
	res = sorted(temp,key = lambda x:x[2],reverse = False)
	for r in res:
		t = r[0]
		cid.append(t)
	for s in res:
		p = s[2]
		exist.append(p)
	for r in cus:
		t = r.BuyingAmount
		targetweighting.append(t)
	for r in cus:
		t = r.TotalAmount
		total.append(t)
	for r in cus:
		t = r.assetAmount
		holding.append(t)
	for r in cus:
		t = r.priority
		priority.append(t)
	for r in cus:
		t = r.designatedQuantity
		designatedQuantity.append(t)
	trans = transationRecord.objects.get(consignmentNo = cus[0].consignmentNo)
	transAmount = trans.transationAmount
	cust = trans.customerNumber
	for r in cus:
		t = r.BuyingAmount
		distribute.append(t)
	for x in range(cust):
		distribute[x]=0
	#cust = 0
	i=0
	flag = []
	while i<cust:
		flag.append(0)
		i+=1
	i=0
	while i<cust:
		j=0
		max=0
		while j<cust:
			if (priority[max]<priority[j] and flag[j]==0) or (flag[max]==1 and flag[j]==0):
				max =j
			j = j + 1
		if(flag[max]==1):
			break
		flag[max]=1
		if(transAmount>=designatedQuantity[max]):
			distribute[max]+=designatedQuantity[max];
			transAmount-=designatedQuantity[max];
		else: 
			distribute[max]+=transAmount;
			transAmount-=transAmount;
		i+=1
		
	num = 1


	while transAmount>0 and num<=cust:
		j=0
		exit_max_index=0
		flag=0
		while j<num:
			if transAmount==0:
				break
			if distribute[j]<targetweighting[j]:
				transAmount = transAmount - 1
				distribute[j] = distribute[j] + 1
				exist[j] =(holding[j]+distribute[j])/(total[j]+distribute[j])
				if exist[j]>exist[exit_max_index]:
					exit_max_index=j
				flag=1
			j = j + 1
		if j<num:
			break
		if flag==0:
		    num = num + 1
		elif num<cust:
			if exist[exit_max_index]>=exist[num]:
			    num = num + 1
	#for x in range(transAmount):
	#for y in range(cust):
	#	while exist[y]<exist[y+1] or distribute[y]<targetweighting[y]:
	#		distribute[y] = distribute[y] + 1
	#		exist[y] = (holding[y]+distribute[y])/(total[y]+distribute[y])
	#		transAmount = transAmount - 1
	#	if exist[y] > exist[y+1] or exist[y] == exist[y+1]:
	#		num = num + 1
	#		for x in range(num):


	#	customer = customerAccount.objects.get(cID=cid[y], consignmentNo=cus[y].consignmentNo)
	#	holding = customer.assetAmount
	#	while holding < (customer.assetAmount+customer.BuyingAmount) and transAmount>0:
	#		holding = holding + 1
	#		transAmount = transAmount - 1
	#		percentage = holding/(customer.assetAmount+holding)
	#		if percentage > exist[y+1]:
	for r in range(cust):
		p = (cid[r],distribute[r])
		resc.append(p)
	con = cus[0].consignmentNo
	fil = result.objects.filter(consignmentNo=con)
	if len(fil)==0:
		for r in resc:
			cid = r[0]
			distr = r[1]
			res = result(consignmentNo=con,cID=cid,allocationInformation=distr)
			res.save()
	#results = distribute
	tra = transationRecord.objects.get(consignmentNo=con)
	tid = tra.id
	tdealer = tra.tdealer
	tID = tra.tID
	tAccount = tra.tAccount
	transactionNo = tra.transactionNo
	transationAmount = tra.transationAmount
	transationPrice = tra.transationPrice
	tdate = tra.tdate
	customerNumber = tra.customerNumber
	transa = transationRecord(id=tid,tdealer=tdealer,tState='True',tID=tID,tAccount=tAccount,consignmentNo=con,transactionNo=transactionNo,transationAmount=transationAmount,transationPrice=transationPrice,tdate=tdate,customerNumber=customerNumber)
	transa.save()
	results = result.objects.filter(consignmentNo=con)
	return results

def AllocationInformation(request,AllocationInfoid_from_url):
	trans = transationRecord.objects.get(id=AllocationInfoid_from_url)
	con = trans.consignmentNo
	cus = result.objects.filter(consignmentNo=con)
	return render_to_response('AllocationInformation.html',locals())

def editAllocation(request,editAllocationid_from_url):
	allocation = result.objects.get(id=editAllocationid_from_url)
	return render_to_response('editAllocation.html',locals())

def SaveEditAllocation(request,SaveEditAllocationid_from_url):
	editallocation = request.GET['allocationInformation']
	rec = result.objects.get(id=SaveEditAllocationid_from_url)
	cons = rec.consignmentNo
	cid = rec.cID
	saveedit = result(id=SaveEditAllocationid_from_url,consignmentNo=cons,cID=cid,allocationInformation=editallocation)
	saveedit.save()
	con = result.objects.get(id=SaveEditAllocationid_from_url)
	cog = con.consignmentNo
	cus = result.objects.filter(consignmentNo=cog)
	return render_to_response('AllocationInformation.html',locals())

def CheckPage(request,checkid_from_url):
	trans = transationRecord.objects.get(id=checkid_from_url)
	consign = trans.consignmentNo
	res = result.objects.filter(consignmentNo=consign)
	che = checkResult.objects.get(consignmentNo=consign)
	return render_to_response('viewInfo.html',locals())

def propertyInfo(request,tID_from_url):
	ass = assetInformation.objects.get(tID=tID_from_url)
	return render_to_response('propertyInfo.html',locals())

#def Allocate(request,allocateid_from_url):
#	return render_to_response('Allocate.html',locals())
	

