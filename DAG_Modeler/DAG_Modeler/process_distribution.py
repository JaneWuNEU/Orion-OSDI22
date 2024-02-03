import numpy as np
import pandas as pd
import os
import sys
import matplotlib.pyplot as plt
sys.path.append(".")
def get_distribution(resource):
    root_path = "D:\\project\\Orion-OSDI22\\DAG_Modeler\\DAG_Modeler/"
    for speed_up in [1,0.1,0.01,0.001]:#np.arange(0.1,1,0.1):
        # if speed_up == 1:
        #     speed_up =1
        # else:
        #     speed_up = round(speed_up,1)

        writer = pd.ExcelWriter(root_path+"overall_dis/org_res="+str(resource)+"_speed="+str(speed_up)+".xlsx")
        for sub_path in ["con_dis","conv_dis","final_dis","real_dis"]:
            path = root_path+"speed="+str(speed_up)+"/"+sub_path+"/Extract_Classify_Frame_"+sub_path+"_1000.txt"
            data = None
            with open(path,"r") as tmp:
                data = tmp.readlines()
            result = {'percentile':[],"value":[]}
            for sample in data:
                tmp = sample.split("#")
                result['percentile'].append(eval(tmp[0]))
                result['value'].append(eval(tmp[1]))
            tmp = pd.DataFrame(result)
            tmp.to_excel(excel_writer=writer,sheet_name=sub_path)
        writer.save()
        writer.close()
#get_distribution(1000)
def get_profile():
    root_path = "./bin/Debug/Video_Analytics_Data/"
    file_list = os.listdir(root_path)
    writer = pd.ExcelWriter(root_path+"profile_details.xlsx")
    for file in file_list:
        resource = file.split("_")[1]
        data = None
        with open(root_path+file) as f:
            data = f.readlines()
        result = {'E2E':[], 'Classify':[],'Shuffle':[], 'Extract':[], 'Split':[]}
        for tmp in data:
            elem = tmp.split(" ")
            result['E2E'].append(int(elem[0].split(":")[1]))
            result['Classify'].append(int(elem[1].split(":")[1]))
            result['Shuffle'].append(int(elem[2].split(":")[1]))
            result['Extract'].append(int(elem[3].split(":")[1]))
            result['Split'].append(int(elem[4].split(":")[1]))
        tmp = pd.DataFrame(result)
        print(tmp)
        tmp.to_excel(excel_writer=writer,sheet_name=str(resource))
    writer.save()
    writer.close()

def compare_e2e_under_mem():
    root_path = "./analyze_accuracy/e2e_comp/"
    for mem in [1000,1800,5000,10240]:
        writer = pd.ExcelWriter(root_path+"mem="+str(mem)+"_speeds.xlsx")
        for speed in [0.001,0.01,0.1,1]:
            # 1. read the estimated and real e2e under specific resources.
            result = {"percentile":[],'est':[],"real":[]}
            file = root_path+"details/est_speed="+str(speed)+"_mem="+str(mem)+".txt"
            with open(file) as f:
                data = f.readlines()
            for tmp in data:
                result['est'].append(int(tmp.split("#")[1]))
                result['percentile'].append(int(tmp.split("#")[0]))

            file = root_path+"details/real_speed="+str(speed)+"_mem="+str(mem)+".txt"
            with open(file) as f:
                data = f.readlines()
            for tmp in data:
                result['real'].append(int(tmp.split("#")[1]))
            tmp = pd.DataFrame(result)
            tmp['ratio'] = tmp['est']/tmp['real']
            tmp.to_excel(excel_writer=writer,sheet_name="speed="+str(speed))
        writer.save()
        writer.close()

def plot_results():
    root_path = "./analyze_accuracy/e2e_comp/"
    plt.rc('font', size=16)
    plt.rcParams["figure.figsize"] = [6, 4]
    legend_font = {'family': 'Arial',
     'weight': 'normal',
     'size': 18,
     }
    for mem in [1000,1800,5000,10240]:
        # plt.figure(mem)
        # xtick = np.round(np.arange(0, 2, 0.2),1)
        # plt.xlabel('Percentile')
        # plt.ylabel('E2E Ratio (estimate/real)')
        tmp = []
        for speed in [0.001, 0.01, 0.1, 1]:
            data = pd.read_excel(root_path+"mem="+str(mem)+"_speeds.xlsx",sheet_name="speed="+str(speed))
            tmp.append(np.average(data['ratio'].values))
        print(np.around(tmp,2))
        #     plt.plot(data['percentile'],data['ratio'],"-.",label="speedup(r)="+str(speed),linewidth=2)
        #     plt.yticks(xtick,xtick)
        # plt.legend(loc="lower center",prop=legend_font,framealpha=0,
        #        columnspacing=0.4,handletextpad=0.2,handlelength=1.5,ncol=2)
        # plt.title("Memsize=" + str(mem) + " (MB)")
        # plt.savefig(root_path+"/figures/mem="+str(mem)+"_speeds.png", bbox_inches='tight', pad_inches=0)


#plot_results()
#compare_e2e_under_mem()
#get_profile()
#plot_results()
