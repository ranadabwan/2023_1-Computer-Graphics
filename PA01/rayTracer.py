#!/usr/bin/env python3
# -*- coding: utf-8 -*
# sample_python aims to allow seamless integration with lua.
# see examples below

import os
import sys
import pdb  # use pdb.set_trace() for debugging
import code # or use code.interact(local=dict(globals(), **locals()))  for debugging.
import xml.etree.ElementTree as ET
import numpy as np
from numpy import uint8
import math
from PIL import Image 

def normalize(vector):
    size = np.sqrt(np.sum(vector**2))
    return vector / size

class Color:
    def __init__(self, R, G, B):
        self.color=np.array([R,G,B]).astype(float)

    # Gamma corrects this color.
    # @param gamma the gamma value to use (2.2 is generally used).
    def gammaCorrect(self, gamma):
        inverseGamma = 1.0 / gamma;
        self.color=np.power(self.color, inverseGamma)

    def toUINT8(self):
        return (np.clip(self.color, 0,1)*255).astype(uint8)

class Shader:
    def __init__(self, diffuseColor, specularColor=np.array([0.,0.,0.]), exponent=0):
        self.diffuseColor=diffuseColor
        self.specularColor=specularColor
        self.exponent=exponent

class Light:
    def __init__(self, position, intensity):
        self.position=position
        self.intensity=intensity

class Camera:              
    def __init__(self, point, direction, up, projDist, viewW, viewH, imgSize):
        self.e=point
        self.w=-direction/np.sqrt(np.sum(direction**2))
        self.u=np.cross(up,self.w)
        self.u=self.u/np.sqrt(np.sum(self.u**2))
        self.v=np.cross(self.w,self.u)
        self.v=self.v/np.sqrt(np.sum(self.v**2))

        # viewD = projD. this project assume projNormal = =viewDir
        self.viewD=projDist
        self.viewW=viewW
        self.viewH=viewH
        self.imgW=imgSize[0]
        self.imgH=imgSize[1]

    def getRay(self, ix, iy):
        uc=iy-self.imgW/2
        vc=-ix+self.imgH/2
        wc=(self.viewD/self.viewW)*self.imgW
        s=self.e+uc*self.u+vc*self.v-wc*self.w
        rayPoint=self.e
        rayVec=s-self.e
        return rayPoint, rayVec

class Sphere:
    def __init__(self, center, radius, shader):
        self.center=center
        self.radius=radius
        self.shader=shader

    def intersect(self, rayPoint, rayVec, minD, maxD):
        p=rayPoint-self.center
        d=normalize(rayVec)
        checkD=(d@p)**2-p@p+self.radius**2 
        t0=np.inf
        hitPoint = np.array([0., 0., 0.])
        hitVector = np.array([0., 0., 0.])
        if checkD>=0:
            t0=-d@p-np.sqrt(checkD)
            t1=-d@p+np.sqrt(checkD)
            hitPoint=rayPoint+t0*d
            hitVector=rayPoint+t0*d-self.center
            if t0<0:
                t0=np.inf
        return hitPoint, hitVector, t0

class Box:
    def __init__(self, minPt, maxPt, shader):
        self.minPt=minPt
        self.maxPt=maxPt
        self.shader=shader
    def intersect(self, rayPoint, rayVec, minD, maxD):
        p=rayPoint
        d=normalize(rayVec)

        tx0, tx1, ty0, ty1, tz0, tz1 = np.inf, np.inf, np.inf, np.inf, np.inf, np.inf
        vx, vy, vz = -1, -1, -1

        if d[0]!=0:
            tx0=(self.minPt[0]-p[0])/d[0]
            tx1=(self.maxPt[0]-p[0])/d[0]
        if d[1]!=0:
            ty0=(self.minPt[1]-p[1])/d[1]
            ty1=(self.maxPt[1]-p[1])/d[1]
        if d[2]!=0:
            tz0=(self.minPt[2]-p[2])/d[2]
            tz1=(self.maxPt[2]-p[2])/d[2]

        if tx0>tx1:
            tmp=tx0
            tx0=tx1
            tx1=tmp
            vx=1
        if ty0>ty1:
            tmp=ty0
            ty0=ty1
            ty1=tmp
            vy=1
        if tz0>tz1:
            tmp=tz0
            tz0=tz1
            tz1=tmp
            vz=1

        tmins=np.array([tx0,ty0,tz0])
        tminIdx=0
        if ty0>tmins[tminIdx]:
            tminIdx=1
        if tz0>tmins[tminIdx]:
            tminIdx=2

        tmaxs=np.array([tx1,ty1,tz1])
        tmaxIdx=0
        if ty1<tmaxs[tmaxIdx]:
            tmaxIdx=1
        if tz1<tmaxs[tmaxIdx]:
            tmaxIdx=2

        hitPoint = np.array([0., 0., 0.])
        hitVector = np.array([0., 0., 0.])
        t0=np.inf
        if tmaxs[tmaxIdx]>tmins[tminIdx]:
            t0=tmins[tminIdx]
            if tminIdx==0:
                normal=np.array([vx,0,0])
            elif tminIdx==1:
                normal=np.array([0,vy,0])
            elif tminIdx==2:
                normal=np.array([0,0,vz])
                
            hitPoint=p+t0*d
            hitVector=normal
        if t0<0:
            t0=np.inf
        return hitPoint, hitVector, t0
        

def checkIntersect(rayPoint, rayVec, SphereList, BoxList):
    tmin=np.inf
    hitPoint = np.array([0., 0., 0.])
    hitVector = np.array([0., 0., 0.])
    for object in SphereList:
        hp, hv, t = object.intersect(rayPoint, rayVec, 0, float('inf'))
        if t<tmin:
            tmin=t
            hitPoint, hitVector = hp, hv
            hitObject=object
    for object in BoxList:
        hp, hv, t = object.intersect(rayPoint, rayVec, 0, float('inf'))
        if t<tmin:
            tmin=t
            hitPoint, hitVector = hp, hv
            hitObject=object

    if tmin == np.inf:
        hitObject=-1

    return tmin, hitPoint, hitVector, hitObject


def parseInput():

    tree = ET.parse(sys.argv[1])
    root = tree.getroot()

    sphereList=[]
    boxList=[]
    lightList=[]  
    shaderDictionary={} 

    # set default values
    viewDir=np.array([0,0,-1]).astype(float)
    viewUp=np.array([0,1,0]).astype(float)
    viewProjNormal=-1*viewDir  # you can safely assume this. (no examples will use shifted perspective camera)
    viewWidth=1.0
    viewHeight=1.0
    projDistance=1.0
    intensity=np.array([1,1,1]).astype(float)  # how bright the light is.

    imgSize=np.array(root.findtext('image').split()).astype(int)

    # set the camera option
    for c in root.findall('camera'):
        if c.find('viewPoint') != None:
            viewPoint=np.array(c.findtext('viewPoint').split()).astype(float)
        if c.find('viewDir') != None:
            viewDir=np.array(c.findtext('viewDir').split()).astype(float)
        if c.find('viewUp') != None:
            viewUp=np.array(c.findtext('viewUp').split()).astype(float)
        if c.find('viewNormal') != None:
            projNormal=np.array(c.findtext('projNormal').split()).astype(float)
        if c.find('projDistance') != None:
            projDistance=np.array(c.findtext('projDistance').split()).astype(float)
        if c.find('viewWidth') != None:
            viewWidth=np.array(c.findtext('viewWidth').split()).astype(float)
        if c.find('viewHeight') != None:
            viewHeight=np.array(c.findtext('viewHeight').split()).astype(float)
        camera = Camera(viewPoint, viewDir, viewUp, projDistance, viewWidth, viewHeight, imgSize)

    # get shader
    for c in root.findall('shader'):
        diffuseColor=np.array(c.findtext('diffuseColor').split()).astype(float)
        if c.get('type')=='Lambertian':
            shaderDictionary[c.get('name')]=Shader(diffuseColor)
        elif c.get('type')=='Phong':
            specularColor=np.array(c.findtext('specularColor').split()).astype(float)
            exponent=np.array(c.findtext('exponent').split()).astype(float)
            shaderDictionary[c.get('name')]=Shader(diffuseColor, specularColor, exponent)  

    # get surface object
    for c in root.findall('surface'):
        objShaderTag=c.find('shader')
        objShaderName=objShaderTag.get('ref')
        objShader=shaderDictionary[objShaderName]

        if c.get('type')=='Sphere':
            objCenter=np.array(c.findtext('center').split()).astype(float)
            objRadius=np.array(c.findtext('radius').split()).astype(float)
            tmpObj=Sphere(objCenter, objRadius, objShader)
            sphereList += [tmpObj]

        if c.get('type')=='Box':
            objMinPt=np.array(c.findtext('minPt').split()).astype(float)
            objMaxPt=np.array(c.findtext('maxPt').split()).astype(float)
            tmpObj=Box(objMinPt, objMaxPt, objShader)
            boxList += [tmpObj]

    # get light
    for c in root.findall('light'):
        lightPosition=np.array(c.findtext('position').split()).astype(float)
        lightIntensity=np.array(c.findtext('intensity').split()).astype(float)
        tmpLight=Light(lightPosition, lightIntensity)
        lightList+= [tmpLight]

    return camera, sphereList, boxList, imgSize, lightList


def main(): 
    #parse the input xml files
    camera, sphereList, boxList, imgSize, lightList = parseInput()

    # Create an empty image
    channels=3
    img = np.zeros((imgSize[1], imgSize[0], channels), dtype=np.uint8)
    img[:,:]=0

    for i in np.arange(imgSize[1]):
        for j in np.arange(imgSize[0]):
            imgColor=np.array([0,0,0])
            # get ray
            rayPoint, rayVec = camera.getRay(i,j)
            tmin, hitPoint, hitVector, hitObject = checkIntersect(rayPoint, rayVec, sphereList, boxList)
            # case: intersection
            if tmin < np.inf:
                normal = normalize(hitVector)
                V = normalize(-rayVec)
                imgColor=np.array([0.,0.,0.])
                for light in lightList:
                    #for Lamberiant
                    I = normalize(light.position-hitPoint)
                    #for Phong
                    h = normalize(I + V)
                    tShadow, hps, hvs, objShadow = checkIntersect(hitPoint, I, sphereList, boxList)
                    if tShadow==np.inf:
                        imgColor+=hitObject.shader.diffuseColor*light.intensity*max([0,I@normal])
                        imgColor+=hitObject.shader.specularColor*light.intensity*(max([0,h@normal])**hitObject.shader.exponent)
        
            #imgColor=255*imgColor
            #for idx in range(3):
            #    if imgColor[idx]>255:
            #        imgColor[idx]=255
            #img[i][j]=imgColor.gammaCorrect(2.2)
            color = Color(imgColor[0], imgColor[1], imgColor[2])
            color.gammaCorrect(2.2)
            img[i][j] = color.toUINT8()

    rawimg = Image.fromarray(img, 'RGB')
    rawimg.save(sys.argv[1]+'test.png')
    
if __name__=="__main__":
    main()