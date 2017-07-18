from Tkinter import *
import os, time, glob

multithread=False
if multithread==True:
    from multiprocessing import Pool
    from multiprocessing.dummy import Pool as ThreadPool

######################################################################################    

def update_path(value,v_or_c,quality,external_source,destination,all_dirs):
    values = [listbox.get(idx) for idx in listbox.curselection()]
    #print ', '.join(values)
    #source_path=[]
    #destination_path=[]
    #for i in values:
        #source_path.append(external_source+'/'+i)
        #destination_path.append(destination+'/'+i)
    #print source_path
    #print quality

    if value==0: #pass #do not re-encode, just copy
    	for i in values:
    	    if os.path.isdir(destination+'/'+i.split('/')[0])==False:os.makedirs(destination+'/'+i.split('/')[0])
            if os.path.isdir(destination+'/'+i)==False:os.makedirs(destination+'/'+i)
            source_files=os.listdir(external_source+'/'+i)
            #for j in range(len(source_files)):
            #    source_files[j]=external_source+'/'+i+'/'+source_files[j]
            print source_files

            destination_files=os.listdir(destination+'/'+i)
	    copy_files=[]
            for j in source_files:
                if j in destination_files: continue
                elif '.mp3' in j or '.aac' in j or '.flac' in j or '.wav' in j:copy_files.append(j)
            if len(copy_files)>0:
                command = 'cp '+external_source+'/'+i+'/{'+','.join(str(x) for x in copy_files)+'} '+destination+'/'+i+'/'
            	print command
            	#os.system(command)
                
                    
    if value==1: #re-encode
    	for i in values:
    	    if os.path.isdir(destination+'/'+i.split('/')[0])==False:os.makedirs(destination+'/'+i.split('/')[0])
            if os.path.isdir(destination+'/'+i)==False:os.makedirs(destination+'/'+i)
            source_files=os.listdir(external_source+'/'+i)
            #for j in range(len(source_files)):
            #    source_files[j]=external_source+'/'+i+'/'+source_files[j]
            #print source_files

            destination_files=os.listdir(destination+'/'+i)
	    copy_files=[]
            if multithread==True: jobs=[]
            for j in source_files:
                if j in destination_files: continue
                elif '.mp3'==j[-4:] or '.aac'==j[-4:] or '.flac'==j[-5:] or '.wav'==j[-4:]:copy_files.append(j)
            if len(copy_files)>0:
                for j in copy_files:
                        print j
                	if v_or_c==1: #variable bitrate, -abr <quality> for abr type, where quality should be approximate bitrate desired, or -V<quality> for true variable bitrate, with -V5 resulting in average 132 kbps, -V2 averaging 200 kbps, and -V0 best quality. between -V0 and V9.999
			    #command="lame -V"+quality+' '+external_source.replace(' ','\ ')+'/'+i.replace(' ','\ ').replace(r'(',r'\(').replace(r')',r'\)')+'/'+j.replace(' ','\ ').replace(r'(',r'\(').replace(r')',r'\)')+' '+destination.replace(' ','\ ')+'/'+i.replace(' ','\ ').replace(r'(',r'\(').replace(r')',r'\)')+'/'+j.replace(' ','\ ').replace(r'(',r'\(').replace(r')',r'\)')
                            command="lame -V"+quality+' "'+external_source+'/'+i.decode('utf-8').encode('utf-8')+'/'+j.decode('utf-8').encode('utf-8')+'" "'+destination+'/'+i.decode('utf-8').encode('utf-8')+'/'+j.decode('utf-8').encode('utf-8')+'"'
                	if v_or_c==2: #constant bitrate, for cbr, -b<quality> is regular encoding, -q0 -b<quality> is highest quality, -f -b<quality> is fastest
        		    #command="lame -b"+quality+' '+external_source.replace(' ','\ ')+'/'+i.replace(' ','\ ').replace(r'(',r'\(').replace(r')',r'\)')+'/'+j.replace(' ','\ ').replace(r'(',r'\(').replace(r')',r'\)')+' '+destination.replace(' ','\ ')+'/'+i.replace(' ','\ ').replace(r'(',r'\(').replace(r')',r'\)')+'/'+j.replace(' ','\ ').replace(r'(',r'\(').replace(r')',r'\)')
                            command=command="lame -b"+quality+' "'+external_source+'/'+i.encode('utf-8')+'/'+j.encode('utf-8')+'" "'+destination+'/'+i.encode('utf-8')+'/'+j.encode('utf-8')+'"'
                    	print command
                        if multithread==False:os.system(command)
                        if multithread==True:jobs.append(command)
                        
            if multithread==True:
                pool=ThreadPool(4)
                pool.map(os.system,jobs)
                pool.close()
                pool.join()

    for i in all_dirs:
        if i not in values and os.path.isdir(destination+'/'+i.decode('utf-8').encode('utf-8')):
            print 'rm -r "'+destination+'/'+i.decode('utf-8').encode('utf-8')+'"'
            os.system('rm -r "'+destination+'/'+i.decode('utf-8').encode('utf-8')+'"')

    return
        
#;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

def update_display(times1,times2,all_dirs,destination):
    #if v1.get()==0:return
    if v1.get()==1:
    	tmp=sorted(zip(all_dirs,times1,times2),key=lambda s: s[0].lower())
        all_dirs=[z for (z,y,x) in tmp]
        times1=[y for (z,y,x) in tmp]
        times2=[x for (z,y,x) in tmp]
    if v1.get()==2:
        tmp=sorted(zip(times1,times2,all_dirs))
        times1=[z for (z,y,x) in tmp][::-1]
        times2=[y for (z,y,x) in tmp][::-1]
        all_dirs=[x for (z,y,x) in tmp][::-1]
    listbox.delete(0,END)
    for i in range(len(all_dirs)):
    	listbox.insert(i,all_dirs[i])
        if os.path.isdir(destination+'/'+all_dirs[i]):listbox.selection_set(i)
    	listbox.update_idletasks()
    #print "Updated"
    return listbox,times1,times2,all_dirs


########################################################################################
root = Tk()
root.title('Music Sync')
root.geometry('400x400')
#root.grid_rowconfigure(0, weight = 1)
#root.grid_columnconfigure(0, weight = 1)

scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)

listbox=Listbox(root,selectmode=MULTIPLE,yscrollcommand=scrollbar.set)
listbox.configure(exportselection=False)

destination='/media/cgarling/SS/Music'
external_source='/media/cgarling/My Passport/Music'
all_dirs=glob.glob(external_source+'/*/*/')

times1=[]
times2=[]
for i in range(len(all_dirs)):
    times1.append(os.path.getmtime(all_dirs[i]))
    times2.append(time.ctime(times1[i]))
    all_dirs[i]=all_dirs[i][len(external_source)+1:-1]

for i in range(len(all_dirs)):
    #Checkbutton(root,text=all_dirs[i],variable=a[all_dirs[i]]).grid(row=i+1,sticky=W)
    listbox.insert(i,all_dirs[i])
    if os.path.isdir(destination+'/'+all_dirs[i]):listbox.selection_set(i)

listbox.pack(side=LEFT,fill=BOTH,expand=1)

v1=IntVar()
v1.set(1)
Radiobutton(root, text="Sortby Name", variable=v1, value=1,indicatoron=0,command=lambda: update_display(times1,times2,all_dirs,destination)).pack(fill=X)
Radiobutton(root, text="Sortby Modified", variable=v1, value=2,indicatoron=0,command=lambda: update_display(times1,times2,all_dirs,destination)).pack(fill=X)

v2=IntVar()
v2.set(1)
Checkbutton(root,text="Re-encode?",variable=v2,onvalue=1,offvalue=0).pack(fill=X)

v3=IntVar()
v3.set(1)
Radiobutton(root, text="VBR", variable=v3, value=1,indicatoron=0).pack(fill=X)
Radiobutton(root, text="CBR", variable=v3, value=2,indicatoron=0).pack(fill=X)

v4=StringVar()
v4.set('2')
e=Entry(root,textvariable=v4)
e.pack(fill=X)

Button(root,text="Update Path",command=lambda: update_path(v2.get(),v3.get(),v4.get(),external_source,destination,all_dirs)).pack(fill=X)

scrollbar.config(command=listbox.yview)
root.mainloop()
#print listbox.get(listbox.curselection())

