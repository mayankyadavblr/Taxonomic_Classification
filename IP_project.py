import tkinter as tk
from tkinter import *
from tkinter import messagebox
#from cgitb import text
#from sqlite3 import Cursor
import pymysql
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean

conn=pymysql.connect(host='localhost',user='root',password='password')
cur=conn.cursor()

def database_setup():
    stmt='create database if not exists taxonomy_database;'
    cur.execute(stmt)
    stmt='use taxonomy_database;'
    cur.execute(stmt)
    #TAXONOMY TABLE    
    stmt='''create table if not exists taxonomy(Slno int primary key auto_increment,
    		kingdom_name varchar(20) not null,
   			phylum_name varchar(20) not null,
   			class_name varchar(20) not null ,
    		orders_name varchar(20) not null ,
            family_name varchar(20) not null,
            genus_name varchar(20) not null,
    		species_name varchar(20) not null unique ,
            common_name varchar(20) not null, 
            population_data int,
            additional_links varchar(50));'''
    cur.execute(stmt)
    conn.commit()
    print('Table created successfully ...')

    #ADMIN TABLE
    stmt='''create table if not exists admin(Slno int auto_increment primary key not null  ,
   		    admin_name varchar(20) not null ,
   			username varchar(20) not null unique ,
  			password varchar(20) not null);'''
    cur.execute(stmt)
    conn.commit()
    print('Admin Table created successfully ...') 

    #REQUEST TABLE
    stmt='''create table if not exists requests(
            Pk int not null primary key auto_increment,
            Slno int,
    		type_of_edit varchar(20) not null,
            kingdom_name varchar(20) not null,
   			phylum_name varchar(20) not null,
   			class_name varchar(20) not null ,
    		orders_name varchar(20) not null,
            family_name varchar(20) not null,
            genus_name varchar(20) not null,
    		species_name varchar(20) not null unique,
            common_name varchar(20),
            population_data int,
            status varchar(20),
            foreign key(Slno) references taxonomy(Slno)
            on delete cascade);'''
    cur.execute(stmt)
    conn.commit()
    print('Request Table created successfully ...') 

    #POPULATION TABLE
    stmt='create table if not exists population_data( Slno int primary key auto_increment,foreign_key int not null,year1 int,year2 int, year3 int, year4 int,year5 int, foreign key (foreign_key) references taxonomy(Slno) on delete cascade);'   
    cur.execute(stmt)
    conn.commit()
    print('Population Table created successfully ...')
    
database_setup()

#MAIN WINDOW
main_window= tk.Tk()
main_window.title('Taxonomy Database')
main_window.geometry("800x600")

#MAIN FRAME
main_frame = tk.Frame(main_window)
main_frame.grid(row=0,rowspan=5,column=0,columnspan=3)

def button_click_admin():
    admin_page = tk.Frame(main_window)
    admin_page.grid(row=0,rowspan=5,column=0,columnspan=3)
    
    def button_click_existing_admin():
        existing_admin_page = tk.Frame(main_window)
        existing_admin_page.grid(row=0,rowspan=5,column=0,columnspan=3)

        def button_click_login():
            cur.execute('select * from admin where password="'+password_input.get()+'" and username="'+username_input.get()+'"')
            r=cur.rowcount
            if r==1: 
                username_input.delete(0,'end')
                password_input.delete(0,'end')
                admin_choice_page=tk.Frame(main_window)
                admin_choice_page.grid(row=0,rowspan=5,column=0,columnspan=3)
            else:
                username_input.delete(0,'end')
                password_input.delete(0,'end')
                print('Wrong username and password')
                return
            
            def button_click_new_entry():
                new_entry_page= tk.Frame(main_window)
                new_entry_page.grid(row=0,rowspan=13,column=0,columnspan=9)
                search_database =tk.Frame(new_entry_page, height=600, width=400)
                search_database.grid(row=1,column=6,columnspan=3,rowspan=9)

                def input_button():
                    kingdom_name = kingdom_input.get()                     
                    phylum_name = phylum_input.get()                   
                    class_name = class_input.get()                   
                    orders_name = orders_input.get()
                    family_name =family_input.get() 
                    genus_name = genus_input.get()                                               
                    species_name = species_input.get()
                    common_name=common_name_input.get()
                    population_data=pop_data_input.get()
                    cur=conn.cursor()
                    cur.execute('insert into taxonomy values(NULL,"'+kingdom_name+'","'+phylum_name+'","'+class_name+'","'+orders_name+'","'+family_name+'","'+genus_name+'","'+species_name+'","'+common_name+'",'+str(population_data)+',"'+'https://en.wikipedia.org/wiki/'+str(common_name.capitalize().replace(' ','_'))+'");')
                    conn.commit()
                    display_box()

                    kingdom_input.delete(0,'end')
                    phylum_input.delete(0,'end')
                    class_input.delete(0,'end')
                    orders_input.delete(0,'end')
                    family_input.delete(0,'end')
                    genus_input.delete(0,'end')
                    species_input.delete(0,'end')
                    common_name_input.delete(0,'end')
                    pop_data_input.delete(0,'end')

                    display_box_initial()
                    messagebox.showinfo('Input','Database Entry Created')

                def edit_button():
                    serial_number = slno_input.get()
                    kingdom_name = kingdom_input.get()                     
                    phylum_name = phylum_input.get()                   
                    class_name = class_input.get()                   
                    orders_name = orders_input.get()
                    family_name =family_input.get() 
                    genus_name = genus_input.get()                                               
                    species_name = species_input.get()
                    common_name=common_name_input.get()
                    population_data=pop_data_input.get()
                    cur=conn.cursor()
                    cur.execute('update taxonomy set kingdom_name="'+kingdom_name+'", phylum_name="'+phylum_name+'",class_name="'+class_name+'",orders_name="'+orders_name+'",family_name="'+family_name+'",genus_name="'+genus_name+'",species_name="'+species_name+'",common_name="'+common_name+'",population_data="'+population_data+'" where Slno="'+serial_number+'";')
                    conn.commit()
                    display_box()
                    
                    slno_input.delete(0,'end')
                    kingdom_input.delete(0,'end')
                    phylum_input.delete(0,'end')
                    class_input.delete(0,'end')
                    orders_input.delete(0,'end')
                    family_input.delete(0,'end')
                    genus_input.delete(0,'end')
                    species_input.delete(0,'end')
                    common_name_input.delete(0,'end')
                    pop_data_input.delete(0,'end')

                    display_box_initial()
                    messagebox.showinfo('Update','Database Entry Updated')

                def delete_button():
                    serial_number = slno_input.get()
                    cur=conn.cursor()
                    cur.execute('delete from taxonomy where Slno="'+serial_number+'";')
                    conn.commit()
                    display_box()

                    slno_input.delete(0, 'end')
                    kingdom_input.delete(0,'end')
                    phylum_input.delete(0,'end')
                    class_input.delete(0,'end')
                    orders_input.delete(0,'end')
                    family_input.delete(0,'end')
                    genus_input.delete(0,'end')
                    species_input.delete(0,'end')
                    common_name_input.delete(0,'end')
                    pop_data_input.delete(0,'end')
 
                    display_box_initial()
                    messagebox.showinfo('Deleted','Database Entry Deleted')

                def button_click_show():
                    stmt='select * from taxonomy;'
                    df=pd.read_sql(stmt, conn)
                    df.to_csv('tk_data.csv',sep=',')
                    os.startfile('tk_data.csv')
                
                def display_box_initial():
                    cur=conn.cursor()
                    cur.execute('SELECT * FROM taxonomy;')
                    rows = cur.fetchall()
                    row_list = list(rows)
                    search_bar.delete(0,'end')
                    search_box.delete(0,'end')
                
                    #THIS PART WAS ME EXTRACTING STUFF FROM THE FETCHALL -> EXPERIMENTAL
                    list_of_lists = []
                    for row in row_list:
                        #insertData = str(row[0])+ '   ' + row[-1]
                        insertlist=list(row[0:9:8])
                        list_of_lists.append(insertlist)
                    
                    #THIS PART IS SUPPOSED TO PUT STUFF IN LISTBOX
                    for lists in list_of_lists:
                        #print(lists)
                        insertData = (str(lists[0])+ '   ' + lists[1])
                        insertlist = []
                        insertlist.append(insertData)
                        #print(insertlist)
                        search_box.insert('end', *insertlist)

                def display_box():
                    cur=conn.cursor()
                    cur.execute('SELECT * FROM taxonomy WHERE kingdom_name LIKE "'+search_bar.get()+'" or phylum_name LIKE "'+search_bar.get()+'" or class_name LIKE "'+search_bar.get()+'" or orders_name LIKE "'+search_bar.get()+'" or family_name LIKE "'+search_bar.get()+'" or genus_name LIKE "'+search_bar.get()+'" or species_name LIKE "'+search_bar.get()+'" or common_name LIKE "'+search_bar.get()+'";')
                    rows = cur.fetchall()
                    row_list = list(rows)
                    search_bar.delete(0,'end')
                    search_box.delete(0,'end')
                    
                    #THIS PART WAS ME EXTRACTING STUFF FROM THE FETCHALL -> EXPERIMENTAL
                    list_of_lists = []
                    for row in row_list:
                        #insertData = str(row[0])+ '   ' + row[-1]
                        insertlist=list(row[0:9:8])
                        list_of_lists.append(insertlist)
                    
                    #THIS PART IS SUPPOSED TO PUT STUFF IN LISTBOX
                    for lists in list_of_lists:
                        #print(lists)
                        insertData = (str(lists[0])+ '   ' + lists[1])
                        insertlist = []
                        insertlist.append(insertData)
                        #print(insertlist)
                        search_box.insert('end', *insertlist)
                               
                def button_click_back():
                    admin_choice_page.grid(row=0,column=0)
                    new_entry_page.grid_forget()

                new_entry_label1=tk.Label(new_entry_page, text='WELCOME TO NEW ENTRY').grid(row=0,column=1)
                
                slno_label = tk.Label(new_entry_page, text='ENTER SERIAL NUMBER (LEAVE EMPTY FOR CREATE)').grid(row=1,column=0)
                slno_input = tk.Entry(new_entry_page)
                slno_input.grid(row=1,column=1)

                kingdom_label = tk.Label(new_entry_page, text='ENTER KINGDOM NAME').grid(row=2,column=0)
                kingdom_input = tk.Entry(new_entry_page)
                kingdom_input.grid(row=2,column=1)
               
                phylum_label = tk.Label(new_entry_page, text='ENTER PHYLUM NAME').grid(row=3,column=0)
                phylum_input = tk.Entry(new_entry_page)
                phylum_input.grid(row=3,column=1)
               
                class_label = tk.Label(new_entry_page, text='ENTER CLASS NAME').grid(row=4,column=0)
                class_input = tk.Entry(new_entry_page)
                class_input.grid(row=4,column=1)
               
                orders_label = tk.Label(new_entry_page, text='ENTER ORDER NAME').grid(row=5,column=0)
                orders_input = tk.Entry(new_entry_page)
                orders_input.grid(row=5,column=1)

                family_label = tk.Label(new_entry_page, text='ENTER FAMILY NAME').grid(row=6,column=0)
                family_input = tk.Entry(new_entry_page)
                family_input.grid(row=6,column=1)

                genus_label = tk.Label(new_entry_page, text='ENTER GENUS NAME').grid(row=7,column=0)
                genus_input = tk.Entry(new_entry_page)
                genus_input.grid(row=7,column=1)

                species_label = tk.Label(new_entry_page, text='ENTER SPECIES NAME').grid(row=8,column=0)
                species_input = tk.Entry(new_entry_page)
                species_input.grid(row=8,column=1)

                common_name_label = tk.Label(new_entry_page, text='ENTER COMMON NAME').grid(row=9,column=0)
                common_name_input = tk.Entry(new_entry_page)
                common_name_input.grid(row=9,column=1)

                pop_data_label = tk.Label(new_entry_page, text='ENTER POPULATION DATA').grid(row=10,column=0)
                pop_data_input = tk.Entry(new_entry_page)
                pop_data_input.grid(row=10,column=1)

                search_hit_enter=tk.Button(search_database,text='SEARCH',command=display_box).grid(row=0,column=2) 
                search_bar=tk.Entry(search_database)
                search_bar.grid(row=0,column=3)
                
                

                button_input_entry = tk.Button(new_entry_page, text="INPUT", command= input_button ).grid(row=12,column=0)
                button_delete_entry=tk.Button(new_entry_page, text='DELETE ENTRY', command= delete_button).grid(row=12,column=1)
                button_edit_entry=tk.Button(new_entry_page, text='EDIT ENTRY', command= edit_button).grid(row=13,column=0)
                button_show_database= tk.Button(new_entry_page, text="SHOW DATABASE",command= button_click_show ).grid(row=13,column=1)
                button_back= tk.Button(new_entry_page, text='BACK', command= button_click_back).grid(row=13,column=2)
                
                
                
                search_box = tk.Listbox(search_database,width=50, height=25)
                search_box.grid(row=1,column=2,columnspan=2)
                display_box_initial()

                admin_choice_page.grid_forget()
            
            def button_click_show():
                stmt='select * from taxonomy;'
                df=pd.read_sql(stmt, conn)
                df.to_csv('tk_data.csv',sep=',')
                os.startfile('tk_data.csv')

            def button_click_edit_request():
                request_page = tk.Frame(main_window)
                request_page.grid(row=0,column=0,rowspan=11,columnspan=9)
                
                def display_box_requests():
                    cur=conn.cursor()
                    cur.execute('SELECT * FROM requests;')
                    rows = cur.fetchall()
                    row_list = list(rows)
                    # search_bar.delete(0,'end')
                    request_box.delete(0,'end')
                
                    #THIS PART WAS ME EXTRACTING STUFF FROM THE FETCHALL -> EXPERIMENTAL
                    list_of_lists = []
                    for row in row_list:
                        #insertData = str(row[0])+ '   ' + row[-1]
                        insertlist=list(row)
                        list_of_lists.append(insertlist)
                    print(list_of_lists)
                    #THIS PART IS SUPPOSED TO PUT STUFF IN LISTBOX
                    for lists in list_of_lists:
                        #print(lists)
                        # insertData = (str(lists[0])+ '   ' + lists[1]+'   ' + lists[2]+'   ' + lists[3]+'   ' + lists[4]+'   ' + lists[5]+'   ' + lists[6]+'   ' + lists[7]+'   ' + lists[8]+'   ' + lists[9]+'   ' + lists[10])
                        insertlist = []
                        insertlist.append(lists)
                        # print(insertlist)
                        # print(lists)
                        request_box.insert('end', *insertlist)
                
                def button_click_back():
                    request_page.grid_forget()
                    admin_choice_page.grid(row=0,column=0)
                
                request_label1 = tk.Label(request_page, text = 'WELCOME TO REQUEST PAGE').grid(row=0,column=3)

                request_box = tk.Listbox(request_page,width=60,height=30)
                request_box.grid(row=2,column=3,rowspan=8)

                def button_click_accept():
                    stmt='select * from requests where pk='+str(req_slno.get())+';'
                    df=pd.read_sql(stmt,conn)
                    if df.iloc[0,2]=='create':
                        stmt='insert into taxonomy(kingdom_name,phylum_name,class_name,orders_name,family_name,genus_name,species_name,common_name,population_data,additional_links) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
                        cur.execute(stmt,(df.iloc[0,3],df.iloc[0,4],df.iloc[0,5],df.iloc[0,6],df.iloc[0,7],df.iloc[0,8],df.iloc[0,9],df.iloc[0,10],df.iloc[0,11],'https://en.wikipedia.org/wiki/'+str(df.iloc[0,10].capitalize().replace(' ','_'))))
                        conn.commit()
                        cur.execute('update requests set status="APPROVED" where pk='+str(req_slno.get())+';')
                        conn.commit()
                    elif df.iloc[0,2]=='delete':
                        stmt='delete from taxonomy where Slno ='+str(df.iloc[0,1])+';'
                        cur.execute(stmt)    
                        conn.commit()
                        cur.execute('update requests set status="APPROVED" where pk='+str(req_slno.get())+';')
                        conn.commit()
                    elif df.iloc[0,2]=='update':
                        cur.execute('update taxonomy set kingdom_name="'+df.iloc[0,3]+'", phylum_name="'+df.iloc[0,4]+'",class_name="'+df.iloc[0,5]+'",orders_name="'+df.iloc[0,6]+'",family_name="'+df.iloc[0,7]+'",genus_name="'+df.iloc[0,8]+'",species_name="'+df.iloc[0,9]+'",common_name="'+df.iloc[0,10]+'",population_data='+str(df.iloc[0,11])+',additional_links='+'"https://en.wikipedia.org/wiki/'+str(df.iloc[0,10].capitalize().replace(' ','_'))+'" where Slno='+str(df.iloc[0,1])+';')
                        conn.commit()
                        cur.execute('update requests set status="APPROVED" where pk='+str(req_slno.get())+';')
                        conn.commit()
                    display_box_requests()

                def button_click_decline():
                    stmt='select * from requests where pk='+str(req_slno.get())+';'
                    df=pd.read_sql(stmt,conn)
                    cur.execute('update requests set status="DENIED" where pk='+str(req_slno.get())+';')
                    conn.commit()
                    display_box_requests()

                req_slno_label = tk.Label(request_page, text = "ENTER REQUEST TABLE SERIAL NUMBER - ").grid(row=1,column=0)
                req_slno = tk.Entry(request_page)
                req_slno.grid(row=1,column=1)
                accept_button = tk.Button(request_page, text='Accept',command=button_click_accept).grid(row=1,column=2)
                accept_button = tk.Button(request_page, text='Decline',command=button_click_decline).grid(row=1,column=3)
                back_button=tk.Button(request_page,text='Back',command=button_click_back).grid(row=10,column=10)
                
                display_box_requests()
                admin_choice_page.grid_forget()

            def button_click_pop_data():
                pop_data_page = tk.Frame(main_window)
                pop_data_page.grid(row=0,column=0)
                
                def best_fit_line(xs,ys):
                    global slope
                    global y_intercept
                    slope=((mean(xs)*mean(ys))-mean(xs*ys))/((mean(xs)*mean(xs))-(mean(xs*xs)))
                    y_intercept=mean(ys)-slope*mean(xs)
                    return slope and y_intercept
                    
                def button_click_graph_compare():
                    cur=conn.cursor()
                    # try:
                    #     graph_slno=int(input('Enter Serial Number from main table - '))
                    # except:
                    #     print('Enter int value')
                    #     return
                    axis_data='SELECT year1,year2,year3,year4, year5 from population_data where foreign_key='+str(show_pop_compare_slno.get())+';'
                    df=pd.read_sql(axis_data,conn)
                    if not df.empty:
                        populationdata1=df.iloc[0].tolist()
                    else:
                        messagebox.showinfo('Data error','Not enough Data')
                        print('No population data')
                        return
                    ys=np.array(populationdata1,dtype=np.float64)
                    xs=np.arange(1,6)
                    best_fit_line(xs,ys)
                    regression_line=[(slope*x)+y_intercept for x in xs]
                    #print(regression_line)

                    try:
                        populationdata1=df.iloc[0].tolist()
                        years=['year1','year2','year3','year4','current year']
                        plt.plot(years,populationdata1,color='blue',label='yearwise population')
                        plt.legend()
                        if slope>0:
                            plt.plot(years,regression_line,color='green',label='increasing population')
                            plt.legend()
                        else:
                            plt.plot(years,regression_line,color='red',label='decreasing population')
                            plt.legend()
                        plt.show()
                    except:
                        messagebox.showinfo('Data error','Not enough Data')
                        print('Not enough data')

                def button_click_graph_all():
                    cur=conn.cursor()
                    # genus_name_graph=input("Enter the genus for the species' population graph-")
                    #graph for critically endangered species
                    axis_data1='SELECT  population_data,common_name from taxonomy where population_data<1000 and genus_name="'+show_all_graph_genus.get()+'";'
                    df=pd.read_sql(axis_data1, conn)
                    populationdata1=df['population_data'].tolist()
                    commonnames1=df['common_name'].tolist()
                    plt.bar(commonnames1,populationdata1,width=0.1,color='red',label='endangered species')
                    plt.legend()
                    
                    #graph for endangered species
                    axis_data2='SELECT  population_data,common_name from taxonomy where population_data>1000 and population_data<=5000 and genus_name="'+show_all_graph_genus.get()+'";'
                    df=pd.read_sql(axis_data2, conn)
                    populationdata2=df['population_data'].tolist()
                    commonnames2=df['common_name'].tolist()
                    plt.bar(commonnames2,populationdata2,width=0.1,color='blue',label='moderate population')
                    plt.legend()

                    #graph for non-endangered species
                    axis_data3='SELECT  population_data,common_name from taxonomy where population_data>5000 and genus_name="'+show_all_graph_genus.get()+'";'
                    df=pd.read_sql(axis_data3, conn) 
                    populationdata=df['population_data'].tolist()
                    commonnames=df['common_name'].tolist()
                    plt.bar(commonnames,populationdata,width=0.1,color='green',label='healthy population')
                    plt.legend()
                    plt.xlabel('species')
                    plt.ylabel('population')
                    try:
                        plt.show()
                    except:
                        print('something went wrong not enough data')

                def button_click_input():
                    cur.execute('insert into population_data values(NULL,"'+slno_input.get()+'","'+year1.get()+'","'+year2.get()+'","'+year3.get()+'","'+year4.get()+'","'+year5.get()+'");')
                    conn.commit()
                    
                def button_click_update():    
                    cur.execute('update population_data set year1="'+year1.get()+'",year2="'+year2.get()+'",year3="'+year3.get()+'",year4="'+year4.get()+'",year5="'+year5.get()+'" where foreign_key='+slno_input.get()+';')
                    conn.commit()

                def button_click_back():
                    admin_choice_page.grid(row=0,column=0)
                    pop_data_page.grid_forget()

                def display_box_initial():
                    cur=conn.cursor()
                    cur.execute('SELECT * FROM taxonomy;')
                    rows = cur.fetchall()
                    row_list = list(rows)
                    # search_bar.delete(0,'end')
                    search_box.delete(0,'end')
                
                    #THIS PART WAS ME EXTRACTING STUFF FROM THE FETCHALL -> EXPERIMENTAL
                    list_of_lists = []
                    for row in row_list:
                        #insertData = str(row[0])+ '   ' + row[-1]
                        insertlist=list(row[0:9:8])
                        list_of_lists.append(insertlist)
                    
                    #THIS PART IS SUPPOSED TO PUT STUFF IN LISTBOX
                    for lists in list_of_lists:
                        #print(lists)
                        insertData = (str(lists[0])+ '   ' + lists[1])
                        insertlist = []
                        insertlist.append(insertData)
                        #print(insertlist)
                        search_box.insert('end', *insertlist) 
                search_box = tk.Listbox(pop_data_page,width=50, height=25)
                search_box.grid(row=1,column=5,columnspan=2,rowspan=9)
                display_box_initial()
                
                pop_data_label1 = tk.Label(pop_data_page, text = "WELCOME TO POPULATION ANALYSIS").grid(row=0,column=1)
                
                slno_label = tk.Label(pop_data_page, text = 'ENTER MAIN TABLE SERIAL NUMBER HERE -').grid(row=1,column=0)
                slno_input = tk.Entry(pop_data_page)
                slno_input.grid(row=1,column=1) 

                pop1_label = tk.Label(pop_data_page, text = 'ENTER POPULATION FOR YEAR 1 HERE -').grid(row=2,column=0)
                year1 = tk.Entry(pop_data_page)
                year1.grid(row=2,column=1) 

                pop2_label = tk.Label(pop_data_page, text = 'ENTER POPULATION FOR YEAR 2 HERE -').grid(row=3,column=0)
                year2 = tk.Entry(pop_data_page)
                year2.grid(row=3,column=1) 

                pop3_label = tk.Label(pop_data_page, text = 'ENTER POPULATION FOR YEAR 3 HERE -').grid(row=4,column=0)
                year3 = tk.Entry(pop_data_page)
                year3.grid(row=4,column=1) 

                pop4_label = tk.Label(pop_data_page, text = 'ENTER POPULATION FOR YEAR 4 HERE -').grid(row=5,column=0)
                year4 = tk.Entry(pop_data_page)
                year4.grid(row=5,column=1)

                pop5_label = tk.Label(pop_data_page, text = 'ENTER POPULATION FOR YEAR 5 HERE -').grid(row=6,column=0)
                year5 = tk.Entry(pop_data_page)
                year5.grid(row=6,column=1) 
                
                input_button = tk.Button(pop_data_page,text='INPUT',command=button_click_input).grid(row=7,column=1)
                update_button = tk.Button(pop_data_page,text = "UPDATE", command = button_click_update).grid(row=7,column=2)

                show_all_label = tk.Label(pop_data_page, text = 'ENTER GENUS NAME').grid(row=8,column=0)
                show_all_button= tk.Button(pop_data_page,text='SHOW ALL POPULATION',command=button_click_graph_all).grid(row=9,column=1)
                show_all_graph_genus=tk.Entry(pop_data_page)
                show_all_graph_genus.grid(row=8,column=1)

                show_all_label = tk.Label(pop_data_page, text = 'ENTER SLNO OF SPECIES').grid(row=10,column=0)
                show_pop_compare_slno=tk.Entry(pop_data_page)
                show_pop_compare_slno.grid(row=10,column=1)
                show_one_button= tk.Button(pop_data_page,text='SHOW POPULATION COMPARISION',command=button_click_graph_compare).grid(row=11,column=1)

                back_button = tk.Button(pop_data_page,text="BACK",command=button_click_back).grid(row=12,column=1)
                admin_choice_page.grid_forget() 
            
            def button_click_back():
                existing_admin_page.grid(row=0,column=0)
                admin_choice_page.grid_forget()

            label_admin_choice=tk.Label(admin_choice_page,text='WELCOME TO ADMIN CHOICE').grid(row=0,column=4,columnspan=2)
            button_new_entry= tk.Button(admin_choice_page, text='NEW ENTRY',command=button_click_new_entry).grid(row=2,column=2)
            button_show_entry= tk.Button(admin_choice_page, text='SHOW DATABASE',command=button_click_show).grid(row=2,column=3)
            button_edit_request= tk.Button(admin_choice_page, text='REQUEST EDIT', command=button_click_edit_request).grid(row=2,column=4)
            button_population_graph= tk.Button(admin_choice_page, text='POPULATION ANALYSIS',command=button_click_pop_data).grid(row=2,column=5)
            button_back= tk.Button(admin_choice_page, text='BACK',command=button_click_back).grid(row=2,column=6)
            
            existing_admin_page.grid_forget()

        def button_click_back():
            existing_admin_page.grid_forget()
            admin_page.grid(row=0,column=0)
            
        exisiting_admin_label1=tk.Label(existing_admin_page, text='WELCOME TO EXISTING ADMIN').grid(row=0,column=1)
        username_label = tk.Label(existing_admin_page, text='ENTER USERNAME').grid(row=1,column=0)
        username_input = tk.Entry(existing_admin_page)
        username_input.grid(row=1,column=1)
        password_label = tk.Label(existing_admin_page, text='ENTER PASSWORD').grid(row=2,column=0)
        password_input = tk.Entry(existing_admin_page)
        password_input.grid(row=2,column=1)
        button_login = tk.Button(existing_admin_page, text='LOGIN',command=button_click_login).grid(row=2,column=2)
        back_button=tk.Button(existing_admin_page,text='Back',command=button_click_back).grid(row=3,column=0)
        admin_page.grid_forget()

    def button_click_new_admin():
        new_admin_page = tk.Frame(main_window)
        new_admin_page.grid(row=0,column=0,rowspan=11,columnspan=9)
        
        def button_click_back():
            new_admin_page.grid_forget()
            admin_page.grid(row=0,column=0)
        
        def button_click_create_admin():
            s='insert into admin values(NULL,"'+name_input.get()+'","'+username_input.get()+'","'+password_input.get()+'");'
            try:
                cur.execute(s)
                conn.commit()
                print('Account created successfully ...')
                name_input.delete(0,'end')
                username_input.delete(0,'end')
                password_input.delete(0,'end')
                button_click_back()
                #print(line)
            except:
                print('Account Already Exists ...')
                name_input.delete(0,'end')
                username_input.delete(0,'end')
                password_input.delete(0,'end')    
                #print(line) 
     

        new_admin_label1 = tk.Label(new_admin_page, text = 'WELCOME TO NEW ADMIN PAGE').grid(row=0,column=4)

        name_label = tk.Label(new_admin_page, text = 'ENTER NAME HERE ').grid(row=1,column=0)
        name_input = tk.Entry(new_admin_page)
        name_input.grid(row=1,column=1)

        username_label = tk.Label(new_admin_page, text = 'ENTER USERNAME HERE ').grid(row=2,column=0)
        username_input = tk.Entry(new_admin_page)
        username_input.grid(row=2,column=1)
        
        password_label = tk.Label(new_admin_page, text = 'ENTER PASSWORD HERE ').grid(row=3,column=0)
        password_input = tk.Entry(new_admin_page)
        password_input.grid(row=3,column=1)

        create_account_button = tk.Button(new_admin_page, text = 'CREATE NEW ACCOUNT',command=button_click_create_admin).grid(row=4,column=1)
        back_button = tk.Button(new_admin_page, text = 'BACK',command=button_click_back).grid(row=12,column=10)
        admin_page.grid_forget()
            
    def button_click_back():
        admin_page.grid_forget()
        main_frame.grid(row=0,column=0)
        
    admin_label_1=tk.Label(admin_page, text='WELCOME TO ADMIN').grid(row=0,column=1)
    button_existing_admin=tk.Button(admin_page, text='EXISTING ADMIN',command=button_click_existing_admin).grid(row=1,column=1)
    button_new_admin=tk.Button(admin_page, text='NEW ADMIN',command=button_click_new_admin).grid(row=1,column=2)
    back_button=tk.Button(admin_page,text='Back',command=button_click_back).grid(row=3,column=0)
    main_frame.grid_forget()

def button_click_user():
    user_choice_page = tk.Frame(main_window)
    user_choice_page.grid(row=0,rowspan=9,column=0,columnspan=9)


    def button_click_back():
        user_choice_page.grid_forget()
        main_frame.grid(row=0,column=0)

    def button_click_search():
        search_database =tk.Frame(main_window, height=600, width=400)
        search_database.grid(row=1,column=6,columnspan=3,rowspan=9)  
        def button_click_back():
            search_database.grid_forget()
            user_choice_page.grid(row=0,column=0)

        def search_data_listbox():
                cur=conn.cursor()
                cur.execute('SELECT * FROM taxonomy WHERE kingdom_name LIKE "'+search_bar.get()+'" or phylum_name LIKE "'+search_bar.get()+'" or class_name LIKE "'+search_bar.get()+'" or orders_name LIKE "'+search_bar.get()+'" or family_name LIKE "'+search_bar.get()+'" or genus_name LIKE "'+search_bar.get()+'" or species_name LIKE "'+search_bar.get()+'" or common_name LIKE "'+search_bar.get()+'";')
                rows = cur.fetchall()
                row_list = list(rows)
                search_box.delete(0,'end')
                search_bar.delete(0,'end')
            
                #THIS PART WAS ME EXTRACTING STUFF FROM THE FETCHALL -> EXPERIMENTAL
                list_of_lists = []
                for row in row_list:
                    #insertData = str(row[0])+ '   ' + row[-1]
                    insertlist=list(row)
                    list_of_lists.append(insertlist)
                print(list_of_lists)
                #THIS PART IS SUPPOSED TO PUT STUFF IN LISTBOX
                for lists in list_of_lists:
                    #print(lists)
                    # insertData = (str(lists[0])+ '   ' + lists[1]+'   ' + lists[2]+'   ' + lists[3]+'   ' + lists[4]+'   ' + lists[5]+'   ' + lists[6]+'   ' + lists[7]+'   ' + lists[8]+'   ' + lists[9]+'   ' + lists[10])
                    insertlist = []
                    insertlist.append(lists[0:10])
                    # print(insertlist)
                    # print(lists)
                    search_box.insert('end', *insertlist)
                pass

        search_hit_enter=tk.Button(search_database,text='SEARCH',command=search_data_listbox).grid(row=0,column=2) 
        search_bar=tk.Entry(search_database)
        search_bar.grid(row=0,column=3)

        search_box = tk.Listbox(search_database,width=50, height=25)
        search_box.grid(row=1,column=2,columnspan=2,rowspan=11)
        search_data_listbox()
        back_button = tk.Button(search_database,text='BACK',command=button_click_back).grid(row=10,column=10)
        user_choice_page.grid_forget()

    def button_click_show():
                stmt='select * from taxonomy;'
                df=pd.read_sql(stmt, conn)
                df.to_csv('tk_data.csv',sep=',')
                os.startfile('tk_data.csv')

    def button_click_edit_request():
                request_page = tk.Frame(main_window)
                request_page.grid(row=0,column=0,rowspan=13,columnspan=9)

                def button_click_back():
                    request_page.grid_forget()
                    user_choice_page.grid(row=0,column=0)
                
                def button_click_request():
                    cur.execute('insert into requests values(null,'+str(slno_input.get())+',"'+type_of_edit_input.get()+'","'+kingdom_input.get()+'","'+phylum_input.get()+'","'+class_input.get()+'","'+orders_input.get()+'","'+family_input.get()+'","'+genus_input.get()+'","'+species_input.get()+'","'+common_name_input.get()+'",'+str(pop_data_input.get())+',"PENDING");')                    
                    conn.commit()
                    
                    messagebox.showinfo('Requested','Database Entry Requested')
                
                def search_data_listbox():
                    cur=conn.cursor()
                    cur.execute('SELECT * FROM taxonomy WHERE kingdom_name LIKE "'+search_bar.get()+'" or phylum_name LIKE "'+search_bar.get()+'" or class_name LIKE "'+search_bar.get()+'" or orders_name LIKE "'+search_bar.get()+'" or family_name LIKE "'+search_bar.get()+'" or genus_name LIKE "'+search_bar.get()+'" or species_name LIKE "'+search_bar.get()+'" or common_name LIKE "'+search_bar.get()+'";')
                    rows = cur.fetchall()
                    row_list = list(rows)
                    search_box.delete(0,'end')
                    search_bar.delete(0,'end')
                
                    #THIS PART WAS ME EXTRACTING STUFF FROM THE FETCHALL -> EXPERIMENTAL
                    list_of_lists = []
                    for row in row_list:
                        #insertData = str(row[0])+ '   ' + row[-1]
                        insertlist=list(row)
                        list_of_lists.append(insertlist)
                    print(list_of_lists)
                    #THIS PART IS SUPPOSED TO PUT STUFF IN LISTBOX
                    for lists in list_of_lists:
                        #print(lists)
                        # insertData = (str(lists[0])+ '   ' + lists[1]+'   ' + lists[2]+'   ' + lists[3]+'   ' + lists[4]+'   ' + lists[5]+'   ' + lists[6]+'   ' + lists[7]+'   ' + lists[8]+'   ' + lists[9]+'   ' + lists[10])
                        insertlist = []
                        insertlist.append(lists[0:10])
                        # print(insertlist)
                        # print(lists)
                        search_box.insert('end', *insertlist)
                    pass

                def display_box_initial():
                    cur=conn.cursor()
                    cur.execute('SELECT * FROM taxonomy;')
                    rows = cur.fetchall()
                    row_list = list(rows)
                    #search_bar.delete(0,'end')
                    search_box.delete(0,'end')
                
                    #THIS PART WAS ME EXTRACTING STUFF FROM THE FETCHALL -> EXPERIMENTAL
                    list_of_lists = []
                    for row in row_list:
                        #insertData = str(row[0])+ '   ' + row[-1]
                        insertlist=list(row[0:9:8])
                        list_of_lists.append(insertlist)
                    
                    #THIS PART IS SUPPOSED TO PUT STUFF IN LISTBOX
                    for lists in list_of_lists:
                        #print(lists)
                        insertData = (str(lists[0])+ '   ' + lists[1])
                        insertlist = []
                        insertlist.append(insertData)
                        #print(insertlist)
                        search_box.insert('end', *insertlist)  

                request_label1 = tk.Label(request_page, text = 'WELCOME TO REQUEST PAGE').grid(row=0,column=0)

                type_of_edit_label = tk.Label(request_page, text='ENTER TYPE OF EDIT (CREATE/UPDATE/DELETE)').grid(row=1,column=0)
                type_of_edit_input = tk.Entry(request_page)
                type_of_edit_input.grid(row=1,column=1)

                slno_label = tk.Label(request_page, text='ENTER SERIAL NUMBER (NULL INCASE OF CREATE)').grid(row=2,column=0)
                slno_input = tk.Entry(request_page)
                slno_input.grid(row=2,column=1)

                kingdom_label = tk.Label(request_page, text='ENTER KINGDOM NAME').grid(row=3,column=0)
                kingdom_input = tk.Entry(request_page)
                kingdom_input.grid(row=3,column=1)
               
                phylum_label = tk.Label(request_page, text='ENTER PHYLUM NAME').grid(row=4,column=0)
                phylum_input = tk.Entry(request_page)
                phylum_input.grid(row=4,column=1)
               
                class_label = tk.Label(request_page, text='ENTER CLASS NAME').grid(row=5,column=0)
                class_input = tk.Entry(request_page)
                class_input.grid(row=5,column=1)
               
                orders_label = tk.Label(request_page, text='ENTER ORDER NAME').grid(row=6,column=0)
                orders_input = tk.Entry(request_page)
                orders_input.grid(row=6,column=1)

                family_label = tk.Label(request_page, text='ENTER FAMILY NAME').grid(row=7,column=0)
                family_input = tk.Entry(request_page)
                family_input.grid(row=7,column=1)

                genus_label = tk.Label(request_page, text='ENTER GENUS NAME').grid(row=8,column=0)
                genus_input = tk.Entry(request_page)
                genus_input.grid(row=8,column=1)

                species_label = tk.Label(request_page, text='ENTER SPECIES NAME').grid(row=9,column=0)
                species_input = tk.Entry(request_page)
                species_input.grid(row=9,column=1)

                common_name_label = tk.Label(request_page, text='ENTER COMMON NAME').grid(row=10,column=0)
                common_name_input = tk.Entry(request_page)
                common_name_input.grid(row=10,column=1)

                pop_data_label = tk.Label(request_page, text='ENTER POPULATION DATA').grid(row=11,column=0)
                pop_data_input = tk.Entry(request_page)
                pop_data_input.grid(row=11,column=1)

                button_input_entry = tk.Button(request_page, text="REQUEST",command=button_click_request ).grid(row=12,column=0)
                back_button=tk.Button(request_page,text='Back',command=button_click_back).grid(row=12,column=10)
                
                search_hit_enter=tk.Button(request_page,text='SEARCH',command=search_data_listbox).grid(row=0,column=2) 
                search_bar=tk.Entry(request_page)
                search_bar.grid(row=0,column=3)

                search_box = tk.Listbox(request_page,width=50, height=25)
                search_box.grid(row=1,column=2,columnspan=2,rowspan=11)
                display_box_initial()

                user_choice_page.grid_forget()

    def button_click_show_graph():
        pop_data_page = tk.Frame(main_window)
        pop_data_page.grid(row=0,column=0)
        
        def best_fit_line(xs,ys):
            global slope
            global y_intercept
            slope=((mean(xs)*mean(ys))-mean(xs*ys))/((mean(xs)*mean(xs))-(mean(xs*xs)))
            y_intercept=mean(ys)-slope*mean(xs)
            return slope and y_intercept
            
        def button_click_graph_compare():
            cur=conn.cursor()
            # try:
            #     graph_slno=int(input('Enter Serial Number from main table - '))
            # except:
            #     print('Enter int value')
            #     return
            axis_data='SELECT year1,year2,year3,year4, year5 from population_data where foreign_key='+str(show_pop_compare_slno.get())+';'
            df=pd.read_sql(axis_data,conn)
            if not df.empty:
                populationdata1=df.iloc[0].tolist()
            else:
                print('No population data')
                return
            ys=np.array(populationdata1,dtype=np.float64)
            xs=np.arange(1,6)
            best_fit_line(xs,ys)
            regression_line=[(slope*x)+y_intercept for x in xs]
            #print(regression_line)

            try:
                populationdata1=df.iloc[0].tolist()
                years=['year1','year2','year3','year4','current year']
                plt.plot(years,populationdata1,color='blue')
                if slope>0:
                    plt.plot(years,regression_line,color='green',label='increasing population')
                    plt.legend()
                else:
                    plt.plot(years,regression_line,color='red',label='decreasing population')
                    plt.legend()
                plt.show()
            except:
                print('Not enough data')
                

        def button_click_graph_all():
            cur=conn.cursor()
            # genus_name_graph=input("Enter the genus for the species' population graph-")
            #graph for critically endangered species
            axis_data1='SELECT  population_data,common_name from taxonomy where population_data<1000 and genus_name="'+show_all_graph_genus.get()+'";'
            df=pd.read_sql(axis_data1, conn)
            populationdata1=df['population_data'].tolist()
            commonnames1=df['common_name'].tolist()
            plt.bar(commonnames1,populationdata1,width=0.1,color='red',label='endangered species')
            plt.legend()
            #graph for endangered species
            axis_data2='SELECT  population_data,common_name from taxonomy where population_data>1000 and population_data<=5000 and genus_name="'+show_all_graph_genus.get()+'";'
            df=pd.read_sql(axis_data2, conn)
            populationdata2=df['population_data'].tolist()
            commonnames2=df['common_name'].tolist()
            plt.bar(commonnames2,populationdata2,width=0.1,color='blue',label='moderate population')
            plt.legend()
            #graph for non-endangered species
            axis_data3='SELECT  population_data,common_name from taxonomy where population_data>5000 and genus_name="'+show_all_graph_genus.get()+'";'
            df=pd.read_sql(axis_data3, conn) 
            populationdata=df['population_data'].tolist()
            commonnames=df['common_name'].tolist()
            plt.bar(commonnames,populationdata,width=0.1,color='green',label='healthy population')
            plt.legend()
            plt.xlabel('species')
            plt.ylabel('population')
            try:
                plt.show()
            except:
                print('something went wrong not enough data')

        def button_click_back():
            user_choice_page.grid(row=0,column=0)
            pop_data_page.grid_forget()

        def display_box_initial():
            cur=conn.cursor()
            cur.execute('SELECT * FROM taxonomy;')
            rows = cur.fetchall()
            row_list = list(rows)
            # search_bar.delete(0,'end')
            search_box.delete(0,'end')
        
            #THIS PART WAS ME EXTRACTING STUFF FROM THE FETCHALL -> EXPERIMENTAL
            list_of_lists = []
            for row in row_list:
                #insertData = str(row[0])+ '   ' + row[-1]
                insertlist=list(row[0:9:8])
                list_of_lists.append(insertlist)
            
            #THIS PART IS SUPPOSED TO PUT STUFF IN LISTBOX
            for lists in list_of_lists:
                #print(lists)
                insertData = (str(lists[0])+ '   ' + lists[1])
                insertlist = []
                insertlist.append(insertData)
                #print(insertlist)
                search_box.insert('end', *insertlist) 
        search_box = tk.Listbox(pop_data_page,width=50, height=25)
        search_box.grid(row=1,column=5,columnspan=2,rowspan=9)
        display_box_initial()
        
        pop_data_label1 = tk.Label(pop_data_page, text = "WELCOME TO POPULATION ANALYSIS").grid(row=0,column=1)

        show_all_label = tk.Label(pop_data_page, text = 'ENTER GENUS NAME').grid(row=1,column=0)
        show_all_button= tk.Button(pop_data_page,text='SHOW ALL POPULATION',command=button_click_graph_all).grid(row=2,column=1)
        show_all_graph_genus=tk.Entry(pop_data_page)
        show_all_graph_genus.grid(row=1,column=1)

        show_all_label = tk.Label(pop_data_page, text = 'ENTER SLNO OF SPECIES').grid(row=3,column=0)
        show_pop_compare_slno=tk.Entry(pop_data_page)
        show_pop_compare_slno.grid(row=3,column=1)
        show_one_button= tk.Button(pop_data_page,text='SHOW POPULATION COMPARISION',command=button_click_graph_compare).grid(row=4,column=1)

        back_button = tk.Button(pop_data_page,text="BACK",command=button_click_back).grid(row=5,column=1)
        user_choice_page.grid_forget() 
    
    def button_click_back():
        main_frame.grid(row=0,column=0)
        user_choice_page.grid_forget()

    user_label_1 = tk.Label(user_choice_page, text='WELCOME TO USER').grid(row=0,column=1)
    
    search_button = tk.Button(user_choice_page, text='SEARCH',command=button_click_search).grid(row=1,column=1)
    show_button = tk.Button(user_choice_page, text='SHOW',command=button_click_show).grid(row=2,column=1)
    request_button = tk.Button(user_choice_page, text='REQUEST',command=button_click_edit_request).grid(row=3,column=1)
    graph_button = tk.Button(user_choice_page, text='GRAPH',command=button_click_show_graph).grid(row=4,column=1)
    back_button=tk.Button(user_choice_page,text='Back',command=button_click_back).grid(row=10,column=10)

    main_frame.grid_forget()


#MAIN FRAME CONTENTS
Label1= tk.Label(main_frame, text='Welcome to Taxonomy')
Label1.grid(row=0,column=1)

button1 = tk.Button(main_frame, text='Admin Login', command=button_click_admin)
button1.grid(row=1,column=1)

button2 = tk.Button(main_frame, text='User Login', command=button_click_user)
button2.grid(row=1,column=2)

#LOOP
main_window.mainloop()