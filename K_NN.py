#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 19:02:36 2019

@author: muss
"""
import pandas as pd
import math

def init():
    veriler = pd.read_csv("wine1.csv");
    satir = []
    veriler_satir = []

    test_data = [13.52,3.17,2.72,23.5,97,1.55,0.52,0.5,0.55,4.35,0.89,2.06,520,3]
    print("Test Verisi : " + str(test_data))
    # veriler satır satır işlenecek
    for j in range(len(veriler)):
        for i in range(14):
            satir.append(veriler.iloc[j,i])
        veriler_satir.append(satir)
        satir = []

    # Mesafesi Hesaplanmıs Veriler
    mesafeler = mesafeHesapla(veriler_satir, test_data)
    # mesafeler[0] = [4.1400483088968905, 'Iris-setosa']

    #Mesafelerin sıralanması

    siralanmis_mesafeler = sirala(mesafeler)
    # [0.31622776601683766, 'Iris-virginica']

    # 1 / uzaklıgın karesi eklenmis mesafeler dizisi
    agirlikli_dizi = agirlikHesapla(siralanmis_mesafeler)
    # agirlik                uzaklık           sınıf
    #[0.613496932515337, 1.276714533480371, 'Iris-versicolor']
    
    k_degeri = input("K Degeri Giriniz : ")
    k_degeri = int(k_degeri)
    siniflandirma_cesidi = input("Agirlikli için : 0\nNormal için : 1 \nIkisinide görmek için : 2\nGiriniz :")
    siniflandirma_cesidi = int(siniflandirma_cesidi)
    
    if(siniflandirma_cesidi == 0):
        # Etiketleme (en yakın k tane degerin agirliklarına gore)
        veri_sinifi_agirlikli = agirlik_ile_etiketleme(k_degeri, agirlikli_dizi)
    elif(siniflandirma_cesidi == 1 ):
        # Etiketleme (en yakın k tane sayısına gore)
        veri_sinifi_normal = etiketleme(k_degeri, siralanmis_mesafeler)
    elif(siniflandirma_cesidi == 2):
        veri_sinifi_normal = etiketleme(k_degeri, siralanmis_mesafeler)
        veri_sinifi_agirlikli = agirlik_ile_etiketleme(k_degeri, agirlikli_dizi)

#         Fonksiyonlar

def agirlik_ile_etiketleme(k_degeri, agirlikli_mesafeler):
    
    a_toplam_dizi = []
    for j in range(k_degeri):
        a_toplam = 0
        a_toplam_dizi_temp = []
        temp_sinif = agirlikli_mesafeler[j][-1]
       #print(agirlikli_mesafeler[j])
        eleman_varmi = False
        # aynı sınıf degerini 1 kez almak için
        for i in range(len(a_toplam_dizi)):
            if temp_sinif in a_toplam_dizi[i]:
                eleman_varmi = True
        # aynı sınıfın agırlıklarının tekrar toplanmasını onlemek için
        if(eleman_varmi == False):   
            a_toplam += agirlikli_mesafeler[j][0]
            
            for i in range((j+1), k_degeri):
                if(temp_sinif == agirlikli_mesafeler[i][-1]):
                    a_toplam += agirlikli_mesafeler[i][0]
                    
            a_toplam_dizi_temp.append(a_toplam)
            a_toplam_dizi_temp.append(temp_sinif)
            
            a_toplam_dizi.append(a_toplam_dizi_temp)
            
    # Agırlıga gore sınıf degeri belirlenmesi
    sinif_degeri = ""
    e_buyuk = 0
    for i in range(len(a_toplam_dizi)):
        if(a_toplam_dizi[i][0] >= e_buyuk):
            e_buyuk = a_toplam_dizi[i][0]
            sinif_degeri = a_toplam_dizi[i][1]
    
    print("\n/////////////// Ağırlıklı Sınıflandırma Sonuçları ////////////////")
    print("\n*** Ağırlık toplamları ve Sınıf isimleri ***\n")
    print(a_toplam_dizi)
    print("-" * 25)
    print( "K Değeri : "+str(k_degeri) +" iken test verisinin sınıfı : " + str(sinif_degeri) + "\nAğırlık Toplamı : " + str(e_buyuk))

    
    return False



def agirlikHesapla(siralanmis_mesafeler):
    
    temp_dizi = []   # diziye elemanları dizi olarak atamak icin
    agirlikli_dizi = []
    
    for i in range(len(siralanmis_mesafeler)): #150 tane mesela
        temp = siralanmis_mesafeler[i][0]
        if(temp != 0):
            temp = (1 / (temp**2))#         1 / uzaklıgın karesi 
        else:
            temp = 1
        temp_dizi.append((temp))
        temp_dizi.append(siralanmis_mesafeler[i][0])
        temp_dizi.append(siralanmis_mesafeler[i][1])
        agirlikli_dizi.append(temp_dizi)
        temp_dizi = []
    return agirlikli_dizi

def etiketleme(k_degeri, siralanmis_mesafeler):#agirlikli yada agirliksız
    sinif_dizi = []
    sinif_ve_eleman_sayilari = []
    
    #burada butun sınıf degerlerini alır (k sayısı kadar)
    for i in range(k_degeri):
        sinif_dizi.append(siralanmis_mesafeler[i][1])
    # ['Iris-virginica', 'Iris-virginica', 'Iris-versicolor' .... vss]

    # hangi sınıftan kaç tane var (sınıf dizideki elemanlar kac kez tekrar ediyor)
    for i in range(len(sinif_dizi)):
        temp = sinif_dizi[i]
        sayac = 1
        temp_sinif = []
        for j in range(i+1, len(sinif_dizi)):
            if(temp == sinif_dizi[j]):
                sayac += 1            # aynı sınıf sayısını tutar
                
        ayni_deger_kontrol = False    # her sınıfı bir kez saymak için

        for k in sinif_ve_eleman_sayilari:
            if(k[0] == temp):
                ayni_deger_kontrol = True

        if(ayni_deger_kontrol == False): # daha once aynı sınıf sayılmamıstır
            temp_sinif.append(temp)
            temp_sinif.append(sayac)
            sinif_ve_eleman_sayilari.append(temp_sinif)
        
    #  sınıf sayısı çok olan sınıf ile etiketle
    e_buyuk = 0
    sinif_degeri = ""
    for i in range(len(sinif_ve_eleman_sayilari)):
        if (sinif_ve_eleman_sayilari[i][1] >= e_buyuk):  # esitkilte son sınıf ile etiketlenir
            e_buyuk = sinif_ve_eleman_sayilari[i][1]
            sinif_degeri = sinif_ve_eleman_sayilari[i][0]
            
    print("\n/////////////// Normal Sınıflandırma Sonuçları ////////////////")
    print("\n****Sınıf Isim ve Sayilari Dizisi****\n")
    print(sinif_ve_eleman_sayilari)
    print("-" * 25)
    print( "K Değeri : "+str(k_degeri) + " iken test verisinin sınıfı : " + str(sinif_degeri))
    
    return sinif_ve_eleman_sayilari


def sirala(mesafeler):
    for i in range(len(mesafeler)):
        for j in range(len(mesafeler) - 1):
            if (mesafeler[j][0] > mesafeler[j+1][0]):
                temp = mesafeler[j]
                mesafeler[j] = mesafeler[j+1]
                mesafeler[j+1] = temp
    return mesafeler

def mesafeHesapla(veriler, test_verisi):
    # veriler[0] = [5.1, 3.5, 1.4, 0.2, 'Iris-setosa']

    mesafeler = []

    for i in range(len(veriler)):    #150
        toplam_temp = 0
        mesafe_sinif_temp = []
        for j in range(len(veriler[i]) - 1):  # 5 - 1 = 4
            fark_karesi = (veriler[i][j] - test_verisi[j]) ** 2
            toplam_temp += fark_karesi
        mesafe_sinif_temp.append(math.sqrt(toplam_temp))
        mesafe_sinif_temp.append(veriler[i][-1])
        mesafeler.append(mesafe_sinif_temp)
    return(mesafeler)

init()













