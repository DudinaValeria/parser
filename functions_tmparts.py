import xml.etree.ElementTree as xml
import xml.etree.ElementTree as ET
import urllib.request
import urllib
import requests
import time
import json
from selenium import webdriver

def get_categories():
    link=''
    headers={}
    r=requests.get(url=link,timeout=30,headers=headers)
    print(r.url)
    r.close()
    p=r.text
    for_deleting='"ArticleSearchParameterList_":"'
    w=p[len(for_deleting):len(p)-1]
    res = list(eval(w))
    dif_names=[]
    for i in res:
        i.get("Name")
        if (i.get("Name")) not in dif_names:
            dif_names.append(i.get("Name"))
    
    root=ET.Element('catalog')
    c_root=ET.SubElement(root,"categories")
    id_cat=[]

    
    #select all different categories
    for j in res :
        if (j.get("Name")=='Категория товара') and j.get("Value") not in id_cat:
            id_cat.append(dict.fromkeys(["id"],str(j.get("ID"))))
            cc_root=ET.SubElement(c_root,"category",attrib=dict.fromkeys(["id"],str(j.get("ID"))))
            cc_root.text=str(j.get("Value"))
    print('end 1')
    return res,root,id_cat,dif_names

def parametrs_for_categories (id_cat, dif_names,res):
    print('begin 2')
    param_cat=[]
    id_cat.pop(0)
    for q in id_cat:
        data_for_data="{'analog':0,'is_main_warehouse':0,'article_search_parameter_list':["
        data_for_data=data_for_data+q.get('id')+','
        null_names=[]
        not_null_names=[]
        for n in dif_names:
                    
            ids=[]
            for j in res:
                if j.get("Name")==n:
                    ids.append(j.get("ID"))
            
            link2=''
            headers2={}  
            with_=[]
            for i in ids:
                s=str(i)+']}'
                data_for_data2=data_for_data+s
                data2={'JSONparameter':data_for_data2}
                try:
                    time.sleep(1)
                    req=requests.get(link2,params=data2,headers=headers2,timeout=5)
                    print('requesting...', q,i)
                except requests.exceptions.ReadTimeout:
                    print("\n Переподключение к серверу \n")
                    time.sleep(60)
                
                with_.append(req.text) 
                        
                        
            count_=0
                        
            for y in with_:
                if y!='[]':
                    count_=count_+len(y)
                if count_==0:
                    null_names.append(n)
                else:
                    not_null_names.append(n) 
        with_names=[]       
        for name in not_null_names:
            if name not in with_names:
                with_names.append(name)
        if with_names!=[]:
            with_names.pop(0)
         
        param_cat.append(with_names)
    print('end 2')
    print(null_names)
    return param_cat
    


def get_goods( res, g_root,param_cat,id_cat):
    
    data_="{'analog':0,'is_main_warehouse':0,'article_search_parameter_list':["
    link2=''
    headers2={}
    
    vsego_tovarov=0     
    missed_goods=0     
    existing_art=[]   
    id_cat.pop(0)
    param_cat.pop(0)
    link4=''
    data4="{'is_main_warehouse': 0, 'Brand_Article_List': [ "                                       
    headers4={}
    br_art=[]
    br_art.append("{'Brand':'LAVR', 'Article':'LN1616'}")
    br_art.append(str({'Brand':'LAVR', 'Article':'LN1324'}))   
    br_art.append(str({'Brand':'LAVR', 'Article':'LN1208'}))  
    br_art.append(str({'Brand':'LAVR', 'Article':'4032'}))
    br_art.append(str({'Brand':'LAVR', 'Article':'4035'}))
    br_art.append(str({'Brand':'PUSEFF', 'Article':'15200M'}))
    br_art.append(str({'Brand':'LIQUIMOLY', 'Article':'35005'}))
    br_art.append(str({'Brand':'LIQUIMOLY', 'Article':'35020'}))
    br_art.append(str({'Brand':'LIQUIMOLY', 'Article':'35027'}))
    for d in br_art:
        
        #data4_for_data=''
        data4_for_data=data4+d+']}'
        data_data4={'JSONparameter':data4_for_data}
       
        try:
            requ=requests.get(link4,params=data_data4,headers=headers4,timeout=30)
        except requests.exceptions.ReadTimeout:
            print("\n Переподключение к серверу \n")
            time.sleep(3)
        except requests.exceptions.ConnectionTimeout:
            time.sleep(60)
        txt=requ.text
        null=None
        missed_goods=0
        vsego_tovarov=0
        existing_art=[]
        
        result=list(eval(txt))
        
        if result is not None:
            for g in result :
                
                flag=1
                vsego_tovarov=vsego_tovarov+1
                photo_path="https://tmparts.ru/StaticContent/ProductImages/"
                brand=str(g.get('brand')).replace(' ','%20')
                
                art=str(g.get('article')).replace(' ','%20')
                link_photo=photo_path+brand+"/"+art+".jpg"
                try:
                    
                    urllib.request.urlopen(link_photo)
                except:
                    continue
                    
                 
                if g.get('article') not in existing_art:
                    
                    existing_art.append(g.get('article'))
                    for b in g.get('warehouse_offers'):
                        
                        if b.get('branch_name')=="Нижний новгород":
                            
                            gg_root=ET.Element("offer")
                            gg_brand=ET.SubElement(gg_root,"brand")
                            gg_brand.text=g.get('brand')
                            gg_artikle=ET.SubElement(gg_root,'article')
                            gg_artikle.text=g.get('article')
                            gg_name=ET.SubElement(gg_root,"name")
                            gg_name.text=g.get('article_name')
                            gg_photo=ET.SubElement(gg_root,'photo')
                            gg_photo.text=(link_photo)
                            gg_category=ET.SubElement(gg_root,'category_id')
                            gg_category.text='4'
                            gg_descr=ET.SubElement(gg_root,'description')
                            #gg_descr.text=str(m)+" : "+str(n.get("Value"))
                            
                            gg_root_tp=ET.Element('variants')
                            
                            gg_root_tp_var=ET.Element('variant')
                            gg_price=ET.SubElement(gg_root_tp_var,"price")
                            gg_price.text=str((round(b.get('price')*float(1.20))))
                            gg_min_part=ET.SubElement(gg_root_tp_var,"min_part")
                            gg_min_part.text=str(b.get('min_part'))
                            gg_quantity=ET.SubElement(gg_root_tp_var,"quantity")
                            gg_quantity.text=str(b.get('quantity'))
                            gg_delivery_period=ET.SubElement(gg_root_tp_var,"delivery_period")
                            gg_delivery_period.text=str(b.get('delivery_period'))
                            flag=0
                            gg_root_tp.append(gg_root_tp_var)
                            gg_root.append(gg_root_tp)
                            g_root.append(gg_root)
                       
                            
               
                    #print("already existing")
                    #for child in g_root.getchildren():
                        #print(g.get('article'),'---',str(child.find("article").text))
                        #if g.get('article')==str(child.find("article").text):
                            #print("yes")
                            #if child.find("description").text.find(str(m))!=-1:
                                #child.find("description").text=child.find("description").text +", "+str(n.get("Value"))
                            #else:   
                                #child.find("description").text=child.find("description").text +"\n"+ str(m)+' : '+str(n.get("Value"))
                            
                                
                            #print(child.find("description").text)
                missed_goods=missed_goods+flag
    for num in range(len(param_cat)):
        
        data_for_data=data_+str(id_cat[num].get("id"))+','
        
        for m in param_cat[num]:
            print(m)
            for n in res:
                if n.get("Name")==m:
                    
                    data_for_data2=data_for_data+str(n.get("ID"))+']}'
                    data2={'JSONparameter':data_for_data2}
                    #get goods with certain [x,y]
                    try:
                        req=requests.get(link2,params=data2,headers=headers2,timeout=30)
                    except requests.exceptions.ReadTimeout:
                        print("\n Переподключение к серверу \n")
                        time.sleep(3)
                    except requests.exceptions.ConnectionTimeout:
                        time.sleep(60)
                        
                   
                    txt=req.text
                    null=None
                    
                    
                    result=list(eval(txt))
                    if result is not None:
                       
                        for g in result :
                            
                            flag=1
                            vsego_tovarov=vsego_tovarov+1
                            photo_path="https://tmparts.ru/StaticContent/ProductImages/"
                            brand=str(g.get('brand')).replace(' ','%20')
                            
                            art=str(g.get('article')).replace(' ','%20')
                            link_photo=photo_path+brand+"/"+art+".jpg"
                            try:
                                
                                urllib.request.urlopen(link_photo)
                            except:
                                continue
                                #print("No photo")
                             
                            if g.get('article') not in existing_art:
                                
                                existing_art.append(g.get('article'))
                                for b in g.get('warehouse_offers'):
                                    
                                    if b.get('branch_name')=="Нижний новгород":
                                        
                                        gg_root=ET.Element("offer")
                                        gg_brand=ET.SubElement(gg_root,"brand")
                                        gg_brand.text=g.get('brand')
                                        gg_artikle=ET.SubElement(gg_root,'article')
                                        gg_artikle.text=g.get('article')
                                        gg_name=ET.SubElement(gg_root,"name")
                                        gg_name.text=g.get('article_name')
                                        gg_photo=ET.SubElement(gg_root,'photo')
                                        gg_photo.text=(link_photo)
                                        gg_category=ET.SubElement(gg_root,'category_id')
                                        gg_category.text=str(id_cat[num].get("id"))
                                        gg_descr=ET.SubElement(gg_root,'description')
                                        gg_descr.text=str(m)+" : "+str(n.get("Value"))
                                        
                                        gg_root_tp=ET.Element('variants')
                                        
                                        gg_root_tp_var=ET.Element('variant')
                                        gg_price=ET.SubElement(gg_root_tp_var,"price")
                                        gg_price.text=str((round(b.get('price')*float(1.20))))
                                        gg_min_part=ET.SubElement(gg_root_tp_var,"min_part")
                                        gg_min_part.text=str(b.get('min_part'))
                                        gg_quantity=ET.SubElement(gg_root_tp_var,"quantity")
                                        gg_quantity.text=str(b.get('quantity'))
                                        gg_delivery_period=ET.SubElement(gg_root_tp_var,"delivery_period")
                                        gg_delivery_period.text=str(b.get('delivery_period'))
                                        flag=0
                                        gg_root_tp.append(gg_root_tp_var)
                                        gg_root.append(gg_root_tp)
                                        g_root.append(gg_root)
                            else:
                                
                                for child in g_root.getchildren():
                                    #print(g.get('article'),'---',str(child.find("article").text))
                                    if g.get('article')==str(child.find("article").text):
                                        #print("yes")
                                        if child.find("description").text.find(str(m))!=-1:
                                            child.find("description").text=child.find("description").text +", "+str(n.get("Value"))
                                        else:   
                                            child.find("description").text=child.find("description").text +"\n"+ str(m)+' : '+str(n.get("Value"))
                                        
                                            
                                        #print(child.find("description").text)
                            missed_goods=missed_goods+flag
    
   
   

                    
    return g_root


res,root,id_cat,dif_names=get_categories()
params_for_cat=[]
param_cat=parametrs_for_categories(id_cat, dif_names,res)  
g_root=ET.SubElement(root,"offers") 
g_root=get_goods(res,g_root,param_cat, id_cat)
tree=ET.ElementTree(root)

tree.write()
     
        
        
        
        

