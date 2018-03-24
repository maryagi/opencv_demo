#encoding:utf-8
import requests
import json

key = {'oem_key':''}
get_resp = requests.get('https://junction-tokyo.minikura.com/v1/minikura/item',params=key)
get_data = get_resp.json()

#GETメソッド取得判定
if get_data['status'] == '1' :
	print "=取得成功==========="
else:
	print "=取得失敗==========="
#print get_data

#box番号が選ばれたとして
x = input("Please Enter BoxNumber: ")
print "BOX" + str(x) + " items:"	

for n in range(0, 10):
	if int(get_data['results'][n]['common02']) == x:
		print "CATEGORY:" + get_data['results'][n]['common01']
		#print "BOX.NO" + get_data['results'][n]['common02']
		print "imageURL:" + get_data['results'][n]['common03']
print "end"
