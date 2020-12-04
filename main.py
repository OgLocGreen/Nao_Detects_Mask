import os
import sys 
"""
path = os.getcwd() + "/Face_Mask_Detection/"
sys.path.append(os.path.abspath(path))
print(path)
import detect_face_mask #detect_face_mask.detection(image)

path = os.getcwd() + "/Face_Mask_Detection/cv2/"
print(path)
sys.path.append(os.path.abspath(path))
import cv2
"""

path = os.getcwd() + "/Face-Mask-Detection/"
sys.path.append(os.path.abspath(path))
print(path)
import detect_mask_image



import paramiko
from scp import SCPClient
import cv2
import time
def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client

if __name__ == "__main__":
    server = "192.168.178.27"
    user = "nao"
    password = "nao"
    port = "22"
    localpath = "~/Desktop/nao"
    remotepath= "/home/nao/recordings/cameras/"
    result_list = []
    result = ""
    no,  mask = 0 , 0

    ssh = createSSHClient(server, port, user, password)
    scp = SCPClient(ssh.get_transport())

    while True:
        print("detection")
        while True: 
            print("waiting for ready")
            scp.get(remote_path = remotepath + "save.txt", local_path = ".")
            save_file = open("save.txt","r")
            save = save_file.read()
            save_file.close()
            if save == "not":
                pass
            elif save == "ready":
                break
            time.sleep(1)

    

        for i in range(0,5):
            print("detect iamge number {}".format(i))
            scp.get(remote_path = remotepath + "image" + str(i) + ".jpg", local_path = ".")
            image = cv2.imread("./image" + str(i) + ".jpg")
            result = detect_mask_image.mask_image(image)
            result_list.append(result)


        print(result_list)
        for num in result_list:
            if num == ["No Mask"]:
                no += 1
            elif num == ["Mask"]:
                mask += 1


        if no > mask:
            result = "no"
        elif mask > no:
            result = "mask"
        else:
            result = "error"


        if os.path.exists("result.txt"):
            os.remove("result.txt")
        result_file = open("result.txt","w+")
        result_file.write(result)
        result_file.close()
        scp.put(remote_path = remotepath, files = "result.txt")
        print(result)


        if os.path.exists("save.txt"):
            os.remove("save.txt")
        save_file = open("save.txt","w+")
        save_file.write("not")
        save_file.close()
        scp.put(remote_path = remotepath, files = "save.txt")
        result_list = []
        no, mask = 0 , 0
        

    