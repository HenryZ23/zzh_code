#encoding=utf-8
#!/usr/bin/python
#edit by zhengzhihang
import commands
import os
import re
try:
    import xml.etree.cElementTree as ET
except:
    import xml.etree.ElementTree as ET
import sys
import smtplib
from email.mime.text import MIMEText   
import commands
import sys
import os
import time
import traceback
from HTMLParser import HTMLParser  
from email.mime.multipart import MIMEMultipart

mail_host="mail2-in.baidu.com"  
mail_user="zhengzhihang"    
mail_pass="3281059ZzH"   
mail_postfix="baidu.com" 

def sendmail(to_list,subject,content,html): 
    print to_list
    me="<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEMultipart('alternative')
    part1 = MIMEText(content, 'plain', 'utf-8')
    part2 = MIMEText(html, 'html', 'utf-8')
    #part3 = MIMEText(html_wf, 'html')
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    msg.attach(part1)
    msg.attach(part2)
    #msg.attach(part3)
    server = smtplib.SMTP()
    server.connect(mail_host)
    server.sendmail(me, to_list, msg.as_string())
    server.close()  
    #print msg.as_string()

def _df_h(df_host, df_file):
    command = 'sshpass -p ps-testing!!! ssh %s \"free -m && df -h && exit\"' % df_host
    (status, output) = commands.getstatusoutput(command) 
    list_output = []
    list_output = output.splitlines() 
    #print list_output
    i = 1
    df_result = '0%'
    mem_result = 0
    for line in list_output:
        i = i + 1
        if i >= 2:
            line_output = re.sub(" +", " ", line)
            #print line_output
            terms = line_output.split(" ")
            #for term in terms:
            #    print term
            #print terms[-1]
            num_home = 0
            if df_file in terms[-1]:
                num_home = num_home +1
                #print line_output
                #print terms[-2]
                df_result = terms[-2]
            elif "Mem:" in terms[0]:
                #print terms
                #print float(terms[1])
                #print float(terms[2])
                #print float(terms[-1])
                mem_used = (float(terms[2])/float(terms[1]))*100
                cache_used = (float(terms[-1])/float(terms[2]))*100
                #print 'cache_used' + str(cache_used)
                #print mem_used
                #mem_result = terms[3]
                mem_result = str("%.2f"%mem_used) + '%'
                cache_result = str("%.2f"%cache_used) + '%' 
                #print mem_result
    return [df_result, mem_result, cache_result]

if __name__ == '__main__':
    try:
        tree = ET.parse("host.xml")
        root = tree.getroot()
    except Exception, e:
        #print "Error:cannot parse file"
        sys.exit(1)
    #print root.tag, "---", root.attrib
    #for child in root:
       #print child.tag, "---", child.attrib
    output_str = ""
    warning_html = ""
    mem_statistics_warning_title = "AC测试：内存和磁盘空间需清理机器"
    mem_statistics_title = "AC测试机器内存和磁盘空间统计"
    task_title = "任务"
    component_title = "组件"
    host_title = "机器"
    memory_title = "内存使用量"
    disk_space_title = "硬盘空间使用量"
    cache_title = "cache内存占用量"
    orange = "橙色框"
    hi_content0 = "Hi,AC值周生:"
    hi_content1 = "&nbsp&nbsp&nbsp&nbsp&nbsp注意！！！以下ac测试机器需要清理空间，请及时处理，谢谢！"
    output_str +="<font>%s<br/></font>" % hi_content0
    output_str +="<font>%s</font>" % hi_content1
    output_str +="<font color=#FF9966>%s</font>" %orange
    output_str +="<font>%s</font>" % "为需清理项"
    output_str += "</table><table width=\"95%\"  cellpadding=\"1\"  style=\"table-layout:fixed;\" >"
    output_str += "<tr><td height=\"40\" colspan=\"6\" class=\"tab6\" style=\"text-align:center;\"><p><strong>%s</strong></p></td></tr>" % (mem_statistics_title)
    output_str += "<tr bgcolor=#E6E6FA><th height=\"20\" colspan=\"1\" class=\"tab3\" style=\"text-align:center;\">%s</th>\
				       <th height=\"20\" colspan=\"1\" class=\"tab3\" style=\"text-align:center;\">%s</th>\
                                       <th height=\"20\" colspan=\"1\" class=\"tab3\" style=\"text-align:center;\">%s</th>\
                                       <th height=\"20\" colspan=\"1\" class=\"tab3\" style=\"text-align:center;\">%s</th>\
                                       <th height=\"20\" colspan=\"1\" class=\"tab3\" style=\"text-align:center;\">%s</th>\
                                       <th height=\"20\" colspan=\"1\" class=\"tab3\" style=\"text-align:center;\">%s</th></tr>" %(task_title, component_title, host_title, disk_space_title, memory_title,cache_title)
    warning_html += "</table><table width=\"95%\"  cellpadding=\"1\"  style=\"table-layout:fixed;\" >"
    warning_html += "<tr><td height=\"40\" colspan=\"4\" class=\"tab4\" style=\"text-align:center;\"><p><strong>%s</strong></p></td></tr>" % (mem_statistics_warning_title)
    warning_html += "<tr bgcolor=#E6E6FA><th height=\"20\" colspan=\"1\" class=\"tab3\" style=\"text-align:center;\">%s</th>\
                                       <th height=\"20\" colspan=\"1\" class=\"tab3\" style=\"text-align:center;\">%s</th>\
                                       <th height=\"20\" colspan=\"1\" class=\"tab3\" style=\"text-align:center;\">%s</th>\
                                       <th height=\"20\" colspan=\"1\" class=\"tab3\" style=\"text-align:center;\">%s</th></tr>" %(host_title, disk_space_title, memory_title, cache_title)
    warning_host_list = []
    warning_flag = 0
    for task in root.findall('task'):
        task_name =  task.get('name')
        for comp in task.findall('component'):
            comp_name =  comp.get('name')
            host = comp.find('host').text
            file = comp.find('file').text
            #print host
            #print file
            [df_num, mem_num, cache_num] = _df_h(host, file)
            output_str += "<tr bgcolor=#FFF0F5><td height=\"20\" colspan=\"1\" class=\"tab3\" style=\"text-align:center;\">%s</td><td height=\"20\" colspan=\"1\" class=\"tab3\" style=\"text-align:center;\">%s</td><td height=\"20\" colspan=\"1\" class=\"tab3\" style=\"text-align:center;\">%s</td><td height=\"20\" colspan=\"1\" class=\"tab3\" style=\"text-align:center;\">%s</td><td height=\"20\" colspan=\"1\" class=\"tab3\" style=\"text-align:center;\">%s</td><td height=\"20\" colspan=\"1\" class=\"tab3\" style=\"text-align:center;\">%s</td></tr>" % (str(task_name).replace(' ',''), str(comp_name).replace(' ',''), str(host).replace(' ',''), str(df_num).replace(' ',''), str(mem_num).replace(' ',''), str(cache_num).replace(' ','')) 
            #print task_name + " " + comp_name + " " + "Memory Used" + " " + df_num + " " + "neicun Available" + " " +  str(mem_num)
            #if int(mem_num) < 3000:
            if (mem_num > '90%') and (cache_num < '50%'):
                warning_flag = 1
                if host not in warning_host_list:
                    warning_host_list.append(host)
                    if df_num > '90%':
                        warning_html += "<tr bgcolor=#FFF0F5><td height=\"20\" colspan=\"1\" class=\"tab3\" style=\"text-align:center;\">%s</td><td bgcolor=#FF9966 height=\"20\" colspan=\"1\" class=\"tab3\" style=\"text-align:center;\">%s</td><td bgcolor=#FF9966 height=\"20\" colspan=\"1\" class=\"tab3\" style=\"text-align:center;\">%s</td><td bgcolor=#FFF0F5 height=\"20\" colspan=\"1\" class=\"tab3\" style=\"text-align:center;\">%s</td></tr>" % (str(host).replace(' ', ''), str(df_num).replace(' ', ''), str(mem_num).replace(' ', ''),str(cache_num).replace(' ','')) 
                    else:
                        warning_html += "<tr bgcolor=#FFF0F5><td height=\"20\" colspan=\"1\" class=\"tab3\" style=\"text-align:center;\">%s</td><td height=\"20\" colspan=\"1\" class=\"tab3\" style=\"text-align:center;\">%s</td><td bgcolor=#FF9966 height=\"20\" colspan=\"1\" class=\"tab3\" style=\"text-align:center;\">%s</td><td bgcolor=#FFF0F5 height=\"20\" colspan=\"1\" class=\"tab3\" style=\"text-align:center;\">%s</td></tr>" % (str(host).replace(' ', ''), str(df_num).replace(' ', ''), str(mem_num).replace(' ', ''), str(cache_num).replace(' ','')) 
            #print "\n"
            elif df_num > '90%':
                warning_flag = 1
                if host not in warning_host_list:
                    warning_host_list.append(host)
                    warning_html += "<tr bgcolor=#FFF0F5><td height=\"20\" colspan=\"1\" class=\"tab3\" style=\"text-align:center;\">%s</td><td bgcolor=#FF9966 height=\"20\" colspan=\"1\" class=\"tab3\" style=\"text-align:center;\">%s</td><td height=\"20\" colspan=\"1\" class=\"tab3\" style=\"text-align:center;\">%s</td><td bgcolor=#FFF0F5 height=\"20\" colspan=\"1\" class=\"tab3\" style=\"text-align:center;\">%s</td></tr>" % (str(host).replace(' ', ''), str(df_num).replace(' ', ''), str(mem_num).replace(' ', ''),str(cache_num).replace(' ','')) 
    output_str = warning_html + output_str
    output_str += "<font></br></br></br>%s</br></font>" % "附："
    email_command = 'curl "http://zhiban.baidu.com/RotaApi/getDNById?id=61151"'
    (email_status, email_output) = commands.getstatusoutput(email_command)
    #print email_status
    email_output_strs = str(email_output).split('\n')
    email_output_str = email_output_strs[-1][:-1]
    print email_output_str
    #shiyan_str ='296111764'
    #mail_list_str = 'zhengzhihang@baidu.com'
    mail_list_str = 'zhengzhihang@baidu.com,wenxiaojun@baidu.com' + ',' + email_output_str + '@baidu.com'
    mail_list = mail_list_str.split(",")
    subject = 'AC测试机器使用空间报警'
    content = ''
    print "warning flag=" + str(warning_flag)
    if(warning_flag == 1):
        sendmail(mail_list,subject,content,output_str)
        
