import numpy as np
import cv2     

def eye_deformation(landmarks,img,state,enlarge_value,img4):
    
    global Leyepts2,Reyepts2,eyeDispts2,LReyePos2,LReyePos1,Mouth_pts2,Mouse_Dist_pts2,Mouth_pos2,nosepts2
    
    LeyePosCenter = np.uint32([(landmarks[36,0]+landmarks[39,0])/2,(landmarks[36,1]+landmarks[39,1])/2])
    ReyePosCenter = np.uint32([(landmarks[42,0]+landmarks[45,0])/2,(landmarks[42,1]+landmarks[45,1])/2])
    facePosCenter = np.uint32([landmarks[30,0]+landmarks[30,1]])
    MouthPosCenter = np.uint32([(landmarks[48,0]+landmarks[54,0])/2,(landmarks[48,1]+landmarks[54,1])/2])
    noseCenter = np.uint32([(landmarks[29,0]+landmarks[30,0])/2,(landmarks[29,1]+landmarks[30,1])/2])
    noseCenter2 = np.uint32([(landmarks[33,0]+landmarks[33,0])/2,(landmarks[33,1]+landmarks[33,1])/2])
    
    Leyepts1 = np.uint32([[landmarks[36,0],landmarks[36,1]],[landmarks[37,0],landmarks[37,1]]
                       ,[landmarks[38,0],landmarks[38,1]],[landmarks[39,0],landmarks[39,1]]
                       ,[landmarks[40,0],landmarks[40,1]],[landmarks[41,0],landmarks[41,1]]
                       ,[(landmarks[36,0]+landmarks[39,0])/2,(landmarks[36,1]+landmarks[39,1])/2]])    
    
    Reyepts1 = np.uint32([[landmarks[42,0],landmarks[42,1]],[landmarks[43,0],landmarks[43,1]]
                       ,[landmarks[44,0],landmarks[44,1]],[landmarks[45,0],landmarks[45,1]]
                       ,[landmarks[46,0],landmarks[46,1]],[landmarks[47,0],landmarks[47,1]]
                       ,[(landmarks[42,0]+landmarks[45,0])/2,(landmarks[42,1]+landmarks[45,1])/2]])
    
    faceDispts1 = np.uint32([[landmarks[0,0],landmarks[0,1]],[landmarks[4,0],landmarks[4,1]]
                        ,[landmarks[6,0],landmarks[6,1]],[landmarks[8,0],landmarks[8,1]]
                        ,[landmarks[10,0],landmarks[10,1]],[landmarks[12,0],landmarks[12,1]]
                        ,[landmarks[16,0],landmarks[16,1]]])
    
    Mouth_pts1 = np.uint32([[landmarks[48,0],landmarks[48,1]],[landmarks[49,0],landmarks[49,1]]
                       ,[landmarks[50,0],landmarks[50,1]],[landmarks[51,0],landmarks[51,1]]
                       ,[landmarks[52,0],landmarks[52,1]],[landmarks[53,0],landmarks[53,1]]
                       ,[landmarks[54,0],landmarks[54,1]],[landmarks[55,0],landmarks[55,1]]
                       ,[landmarks[56,0],landmarks[56,1]],[landmarks[57,0],landmarks[57,1]]
                       ,[landmarks[58,0],landmarks[58,1]],[landmarks[59,0],landmarks[59,1]]
                       ,[(landmarks[48,0]+landmarks[54,0])/2,(landmarks[48,1]+landmarks[54,1])/2]])
    
    nosepts1= np.uint32([[landmarks[28,0],landmarks[28,1]],[landmarks[31,0],landmarks[31,1]]
                       ,[landmarks[32,0],landmarks[32,1]],[landmarks[33,0],landmarks[33,1]]
                       ,[landmarks[34,0],landmarks[34,1]],[landmarks[35,0],landmarks[35,1]]
                       ,[(landmarks[29,0]+landmarks[30,0])/2,(landmarks[29,1]+landmarks[30,1])/2]])
    
    eyeDispts1 = faceDispts1.copy()
    eyeDispts1 = np.append(eyeDispts1,Leyepts1,axis=0)
    eyeDispts1 = np.append(eyeDispts1,Reyepts1,axis=0)
        
    
    if(state==1):
        Leyepts2 = eye_deformation_enlarge_Pos(Leyepts1,LeyePosCenter,enlarge_value)    
        Reyepts2 = eye_deformation_enlarge_Pos(Reyepts1,ReyePosCenter,enlarge_value)
    elif(state==2):
        Leyepts2 = eye_deformation_high_Pos(Leyepts1,LeyePosCenter,enlarge_value)    
        Reyepts2 = eye_deformation_high_Pos(Reyepts1,ReyePosCenter,enlarge_value)
    elif(state==3):
        Leyepts2 = eye_deformation_distance_Pos(Leyepts1,-1,enlarge_value)  
        Reyepts2 = eye_deformation_distance_Pos(Reyepts1,1,enlarge_value)
    elif(state==4):
        faceDispts2 = Face_deformation_pos(faceDispts1,facePosCenter,enlarge_value)
    elif(state==5):
        nosepts2 = nose_deformation_enlarge_Pos(nosepts1,noseCenter,enlarge_value)
    elif(state==6):
        nosepts2 = nose_deformation_Pos(nosepts1,noseCenter2,enlarge_value)
    elif(state==7):
        Mouth_pts2 = eye_deformation_enlarge_Pos(Mouth_pts1,LeyePosCenter,enlarge_value) 
        
        
    if(state==3):
        eyeDispts2 = faceDispts1.copy()
        eyeDispts2 = np.append(eyeDispts2,Leyepts2,axis=0)
        eyeDispts2 = np.append(eyeDispts2,Reyepts2,axis=0)
        initial = trans(img, eyeDispts1)
        img3 = initial.deformation(img, eyeDispts2)
        img4 = initial.deformation(img4, eyeDispts2)
    elif(state==4):
        initial = trans(img, faceDispts1)
        img3 = initial.deformation(img, faceDispts2) 
        img4 = initial.deformation(img4, faceDispts2)
    elif(state==6 or state==5):
        initial = trans(img, nosepts1)
        img3 = initial.deformation(img, nosepts2)
        img4 = initial.deformation(img4, nosepts2)
    elif(state==7):
        initial = trans(img, Mouth_pts1)
        img3 = initial.deformation(img, Mouth_pts2)
        img4 = initial.deformation(img4, Mouth_pts2)
    elif(state==8):
        img3 = img4.copy()
        img3 = colorChange(landmarks,img3,enlarge_value)        
    else:
        LReyePos1 = Leyepts1.copy()
        LReyePos1 = np.append(LReyePos1,Reyepts1,axis=0)
        LReyePos2 = Leyepts2.copy()
        LReyePos2 = np.append(LReyePos2,Reyepts2,axis=0)
        initial = trans(img, LReyePos1)
        img3 = initial.deformation(img, LReyePos2) 
        img4 = initial.deformation(img, LReyePos2)    


    return img3,img4

#調整頂點位置放大縮小

def eye_deformation_enlarge_Pos(pos1,c,enlarge_value):
    p1 = np.empty(shape=(0, 2)) 
    a = np.empty(shape=(0, 2))
    #位移方向
    for idx, point in enumerate(pos1):
        vec1 = np.int32([pos1[idx]-c])
        a = np.append(a,vec1,axis=0)
        dic = normalization(a)
    p1 = pos1 + dic * enlarge_value
    p1 = np.uint32(p1)   
    return p1

#調整頂點位置 眼高

def eye_deformation_high_Pos(pos1,c,enlarge_value):
    a = np.empty(shape=(0, 2))
    for idx, point in enumerate(pos1):
        vec1 = np.int32([pos1[idx]-c])   
        a = np.append(a,vec1,axis=0)
    dic = normalization(a)
    p1 = np.empty(shape=(0, 2))
    #加移動向量
    for idx, point in enumerate(pos1):
        if(idx>0 and idx!=3 and idx!=6):
            pos = np.uint32([pos1[idx]+dic[idx]*enlarge_value])
            p1 = np.append(p1,pos,axis=0)
        else:
            pos = np.uint32([pos1[idx]])
            p1 = np.append(p1,pos,axis=0)
        p1 = np.uint32(p1)
    return p1

def eye_deformation_distance_Pos(pos1,d,enlarge_value):
    dic = np.array([1,0])
    p1 = np.empty(shape=(0, 2))
    #加移動向量
    for idx, point in enumerate(pos1):
        pos = np.uint32([pos1[idx]+ dic * enlarge_value * d])
        p1 = np.append(p1,pos,axis=0)
        p1 = np.uint32(p1)
    return p1

def Face_deformation_pos(pos1,c,enlarge_value):
    dic2 = np.array([-1,1])
    a = np.empty(shape=(0, 2))
    for idx, point in enumerate(pos1):
        vec1 = np.int32([pos1[idx]-c])   
        a = np.append(a,vec1,axis=0)
    dic = normalization(a)
    p1 = np.empty(shape=(0, 2))
    #加移動向量
    for idx, point in enumerate(pos1):
        if(idx>3 and idx!=6):
            pos = np.uint32([pos1[idx]+dic[idx]*enlarge_value*dic2])
            p1 = np.append(p1,pos,axis=0)
        elif(idx>0 and idx!=6 and idx!=3):
            pos = np.uint32([pos1[idx]+dic[idx]*enlarge_value])
            p1 = np.append(p1,pos,axis=0)
        else:
            pos = np.uint32([pos1[idx]])
            p1 = np.append(p1,pos,axis=0)
        p1 = np.uint32(p1)
    return p1

def nose_deformation_enlarge_Pos(pos1,c,enlarge_value):
    print(c)
    a = np.empty(shape=(0, 2))
    #位移方向
    for idx, point in enumerate(pos1):
        vec1 = np.int32([pos1[idx]-c])
        a = np.append(a,vec1,axis=0)
    dic = normalization(a)
    #加移動向量
    p1 = np.empty(shape=(0, 2))
    for idx, point in enumerate(pos1):
        pos = np.uint32([pos1[idx]+dic[idx]*enlarge_value])
        p1 = np.append(p1,pos,axis=0)
    p1 = np.uint32(p1)
    return p1
    

def nose_deformation_Pos(pos1,c,enlarge_value):
    print(c)
    a = np.empty(shape=(0, 2))
    #位移方向
    for idx, point in enumerate(pos1):
        vec1 = np.int32([pos1[idx]-c])
        a = np.append(a,vec1,axis=0)
    dic = normalization(a)
    #加移動向量
    p1 = np.empty(shape=(0, 2))
    for idx, point in enumerate(pos1):
        if(idx!=0 or idx!=5):
            pos = np.uint32([pos1[idx]+dic[idx]*enlarge_value])
            p1 = np.append(p1,pos,axis=0)
        else:
            pos = np.uint32([pos1[idx]])
    p1 = np.uint32(p1)
    return p1

#規一化後的範圍是[-1, 1]
def normalization(data):
    _range = np.max(abs(data))
    return data / _range


class trans():
    def __init__(self, img, pi):#原圖,原座標組
        width, height = img.shape[:2]
        pcth = np.repeat(np.arange(height).reshape(height, 1), [width], axis=1) 
        pctw = np.repeat(np.arange(width).reshape(width, 1), [height], axis=1).T

        self.img_coordinate = np.swapaxes(np.array([pcth, pctw]), 1, 2).T #維度變換
        self.cita = compute_G(self.img_coordinate, pi, height, width)
        self.pi = pi
        self.W, self.A, self.Z = pre_compute_waz(self.pi, height, width, self.img_coordinate)
        self.height = height
        self.width = width

    def deformation(self, img, qi):

        qi = self.pi * 2 - qi
        mapxy = np.swapaxes(np.float32(compute_fv(qi, self.W, self.A, self.Z, self.height, self.width, self.cita, self.img_coordinate)), 0, 1)
        img = cv2.remap(img, mapxy[:, :, 0], mapxy[:, :, 1], borderMode=cv2.BORDER_WRAP, interpolation=cv2.INTER_LINEAR)

        return img
    
def pre_compute_waz(pi, height, width, img_coordinate):
    # height*width*控制点个数
    wi = np.reciprocal(np.power(np.linalg.norm(np.subtract(pi, img_coordinate.reshape(height, width, 1, 2)) + 0.000000001, axis=3),2))

    # height*width*2
    pstar = np.divide(np.matmul(wi,pi), np.sum(wi, axis=2).reshape(height,width,1))

    # height*width*控制点个数*2
    phat = np.subtract(pi, pstar.reshape(height, width, 1, 2))

    z1 = np.subtract(img_coordinate, pstar)
    z2 = np.repeat(np.swapaxes(np.array([z1[:,:,1], -z1[:,:,0]]), 1, 2).T.reshape(height,width,1,2,1), [pi.shape[0]], axis=2)

    # height*width*控制点个数*2*1
    z1 = np.repeat(z1.reshape(height,width,1,2,1), [pi.shape[0]], axis=2)

    # height*width*控制点个数*1*2
    s1 = phat.reshape(height,width,pi.shape[0],1,2)
    s2 = np.concatenate((s1[:,:,:,:,1], -s1[:,:,:,:,0]), axis=3).reshape(height,width,pi.shape[0],1,2)

    a = np.matmul(s1, z1)
    b = np.matmul(s1, z2)
    c = np.matmul(s2, z1)
    d = np.matmul(s2, z2)

    # 重构wi形状
    ws = np.repeat(wi.reshape(height,width,pi.shape[0],1),[4],axis=3)

    # height*width*控制点个数*2*2
    A = (ws * np.concatenate((a,b,c,d), axis=3).reshape(height,width,pi.shape[0],4)).reshape(height,width,pi.shape[0],2,2)

    return wi, A, z1

def compute_fv(qi, W, A, Z, height, width, cita, img_coordinate):   
    qstar = np.divide(np.matmul(W,qi), np.sum(W, axis=2).reshape(height,width,1))
    qhat = np.subtract(qi, qstar.reshape(height, width, 1, 2)).reshape(height, width, qi.shape[0], 1, 2)
    fv_ = np.sum(np.matmul(qhat, A),axis=2)
    fv = np.linalg.norm(Z[:,:,0,:,:],axis=2) / (np.linalg.norm(fv_,axis=3)+0.0000000001) * fv_[:,:,0,:] + qstar
    fv = (fv - img_coordinate) * cita.reshape(height, width, 1) + img_coordinate
    return fv

#衰减系数计算
def compute_G(img_coordinate, pi, height, width, thre = 0.9):
    # thre: 影响系数，数值越大对控制区域外影响越大，反之亦然，取值范围0到无穷大
    max = np.max(pi, 0) #返回每列最大元素
    min = np.min(pi, 0) #返回每列最小元素

    length = np.max(max - min)

    # 计算控制区域中心
    # p_ = (max + min) // 2
    p_ = np.sum(pi,axis=0) // pi.shape[0]

    # 计算控制区域
    minx, miny = min - length
    maxx, maxy = max + length
    minx = minx if minx > 0 else 0
    miny = miny if miny > 0 else 0
    maxx = maxx if maxx < height else height
    maxy = maxy if maxy < width else width

    k1 =(p_ - [0,0])[1] / (p_ - [0,0])[0]
    k2 =(p_ - [height,0])[1] / (p_ - [height,0])[0]
    k4 =(p_ - [0,width])[1] / (p_ - [0,width])[0]
    k3 =(p_ - [height, width])[1] / (p_ - [height, width])[0]
    k = (np.subtract(p_, img_coordinate)[:, :, 1] / (np.subtract(p_, img_coordinate)[:, :, 0] + 0.000000000001)).reshape(height, width, 1)
    k = np.concatenate((img_coordinate, k), axis=2)

    k[:,:p_[1],0][(k[:,:p_[1],2] > k1) | (k[:,:p_[1],2] < k2)] = (np.subtract(p_[1], k[:,:,1]) / p_[1]).reshape(height, width, 1)[:,:p_[1],0][(k[:,:p_[1],2] > k1) | (k[:,:p_[1],2] < k2)]
    k[:,p_[1]:,0][(k[:,p_[1]:,2] > k3) | (k[:,p_[1]:,2] < k4)] = (np.subtract(k[:,:,1], p_[1]) / (width - p_[1])).reshape(height, width, 1)[:,p_[1]:,0][(k[:,p_[1]:,2] > k3) | (k[:,p_[1]:,2] < k4)]
    k[:p_[0],:,0][(k1 >= k[:p_[0],:,2]) & (k[:p_[0],:,2] >= k4)] = (np.subtract(p_[0], k[:,:,0]) / p_[0]).reshape(height, width, 1)[:p_[0],:,0][(k1 >= k[:p_[0],:,2]) & (k[:p_[0],:,2] >= k4)]
    k[p_[0]:,:,0][(k3 >= k[p_[0]:,:,2]) & (k[p_[0]:,:,2] >= k2)] = (np.subtract(k[:,:,0], p_[0]) / (height - p_[0])).reshape(height, width, 1)[p_[0]:,:,0][(k3 >= k[p_[0]:,:,2]) & (k[p_[0]:,:,2] >= k2)]

    cita = np.exp(-np.power(k[:,:,0] / thre,2))
#     cita[minx:maxx,miny:maxy] = 1
    # 如果不需要局部变形，可以把cita的值全置为1
    # cita = 1

    return cita

def createBox(img,points,scale=5,masked=False,cropped = True): #遮罩(嘴唇變顏色)
    if masked:
        mask = np.zeros_like(img)
        mask = cv2.fillPoly(mask,[points],(255,255,255))
        img = cv2.bitwise_and(img,mask)
        # cv2.imshow('Mask',img)
 
 
    if cropped:
        bbox = cv2.boundingRect(points)
        x,y,w,h = bbox
        imgCrop = img[y:y+h,x:x+w]
        imgCrop = cv2.resize(imgCrop,(0,0),None,scale,scale)
        return imgCrop
    else:
        return mask
    
def colorChange(landmarks,img,enlarge_value):
    b=g=0
    r=enlarge_value
    imgLips = createBox(img,landmarks[48:61],8,masked=True,cropped=False)
    imgColorLips = np.zeros_like(imgLips)
    imgColorLips[:] = b,g,r
    imgColorLips = cv2.bitwise_and(imgLips,imgColorLips)
    imgColorLips = cv2.GaussianBlur(imgColorLips,(7,7),10)
    imgColorLips = cv2.addWeighted(img,1,imgColorLips,0.4,0)
    
    return imgColorLips
    
    
