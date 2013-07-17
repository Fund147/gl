from django.db import models

# Create your models here.

class transationRecord(models.Model):
    tdealer = models.CharField(max_length=30)
    tState = models.CharField(max_length=30)
    tID = models.IntegerField()
    tAccount = models.CharField(max_length=30)
    consignmentNo = models.CharField(max_length=30)
    transactionNo = models.CharField(max_length=30)
    transationAmount = models.FloatField()
    transationPrice = models.FloatField()
    tdate = models.CharField(max_length=30)
    customerNumber = models.IntegerField()

class assetInformation(models.Model):
    tID = models.IntegerField()
    aName = models.CharField(max_length=30)
    aClass = models.CharField(max_length=30)
    aMarket = models.CharField(max_length=30)
    currency = models.CharField(max_length=30)
    lotSize = models.FloatField()
    pPrice = models.FloatField()
    tPrice = models.FloatField()

class result(models.Model):
	consignmentNo = models.CharField(max_length=30)
	cID = models.IntegerField()
	allocationInformation = models.FloatField()


class customerAccount(models.Model):
	name = models.CharField(max_length=30)
	cID = models.IntegerField()
	tID = models.IntegerField()
	consignmentNo = models.CharField(max_length=30)
	assetAmount = models.FloatField()
	BuyingAmount = models.FloatField()
	priority = models.IntegerField()
	designatedQuantity = models.FloatField()
	TotalAmount = models.FloatField()
	ExistingPercentage = models.FloatField()

class checkResult(models.Model):
	consignmentNo = models.CharField(max_length=30)
	sName= models.CharField(max_length=30)
	is_pass = models.CharField(max_length=30)
	checkInformation = models.CharField(max_length=100)


class dealer(models.Model):
    dName = models.CharField(max_length=30)
    dID = models.IntegerField()
    password = models.CharField(max_length=30)
    contractInformation = models.CharField(max_length=30)


class supervisor(models.Model):
	sName = models.CharField(max_length=30)
	sID = models.IntegerField()
	password = models.CharField(max_length=30)
	contractInformation = models.CharField(max_length=30)