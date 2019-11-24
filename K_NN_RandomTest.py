#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 19:02:36 2019

@author: muss
"""
import pandas as pd
import math
import random


def init():
    veriler = pd.read_csv("wine1.csv");
    satir = []
    veriler_satir = []

    # veriler satır satır işlenecek
    for j in range(len(veriler)):
        for i in range(14):
            satir.append(veriler.iloc[j,i])
        veriler_satir.append(satir)
        satir = []
    
        
    print("veri sayısı : " + str(len(veriler_satir)))
    # veriler_satir içinden test sayısı kadar veri seçilip çıkarılır
    veriler_satir, test_verileri = verileri_bol(veriler_satir, 45)
    print("veri sayısı testler haric : " + str(len(veriler_satir)))
    #print(test_verileri)
    
    """
    # A test B-C yi egitim için ayır
    print("Toplam Veri Sayısı : " + str(len(veriler_satir)))
    # veriler_satir içinden test sayısı kadar veri seçilip çıkarılır
    veriler_satir, test_verileri = verileri_adil_bol(veriler_satir, sinif_adi=1)
    print("Testler Haric Veri Sayısı : " + str(len(veriler_satir)))
    print("Test Veri Sayısı : " + str(len(test_verileri)))
    """
    
    k_degeri = input("K Degeri Giriniz : ")
    k_degeri = int(k_degeri)
    siniflandirma_cesidi = input("Agirlikli için : 0\nNormal için : 1 \nIkisinide görmek için : 2\nGiriniz :")
    siniflandirma_cesidi = int(siniflandirma_cesidi)

    # test verilerini gonder kontrol et
    
    normal_knn_sayac = 0
    agirlikli_knn_sayac = 0
    
    for test_verisi in test_verileri:
        
        siralanmis_mesafeler, agirlikli_dizi = mesafe_siralama_agirlik_hesapla(veriler_satir, test_verisi)
        
        if(siniflandirma_cesidi == 0):
            # Etiketleme (en yakın k tane degerin agirliklarına gore)
            
            veri_sinifi_agirlikli = agirlik_ile_etiketleme(k_degeri, agirlikli_dizi)
            print("Test Verisi : " + str(test_verisi))
            if(veri_sinifi_agirlikli == test_verisi[-1]):
                agirlikli_knn_sayac += 1
                
        elif(siniflandirma_cesidi == 1 ):
            # Etiketleme (en yakın k tane sayısına gore)
            
            veri_sinifi_degeri = etiketleme(k_degeri, siralanmis_mesafeler)
            print("Test Verisi : " + str(test_verisi))
            if(veri_sinifi_degeri == test_verisi[-1]):
                normal_knn_sayac += 1
                
        elif(siniflandirma_cesidi == 2):
            veri_sinifi_degeri = etiketleme(k_degeri, siralanmis_mesafeler)
            if(veri_sinifi_degeri == test_verisi[-1]):
                normal_knn_sayac += 1
            veri_sinifi_agirlikli = agirlik_ile_etiketleme(k_degeri, agirlikli_dizi)
            if(veri_sinifi_agirlikli == test_verisi[-1]):
                agirlikli_knn_sayac += 1
    if(len(test_verileri) != 0):
        print("\nNormal K-NN Doğruluk Yüzdesi : % " + str((normal_knn_sayac / len(test_verileri)) * 100))
        print("Ağırlıklı K-NN Doğruluk Yüzdesi : % " + str((agirlikli_knn_sayac / len(test_verileri)) * 100))

        

#         Fonksiyonlar

# mesafe hesabı - sıralama ve ağırlık hesabı
def mesafe_siralama_agirlik_hesapla(veriler_satir, test_verisi):
    # Mesafesi Hesaplanmıs Veriler
    mesafeler = mesafeHesapla(veriler_satir, test_verisi)
    # mesafeler[0] = [4.1400483088968905, 'Iris-setosa']
    
    #Mesafelerin sıralanması
    siralanmis_mesafeler = sirala(mesafeler)
    # [0.31622776601683766, 'Iris-virginica']

    # 1 / uzaklıgon karesi eklenmis mesafeler dizisi
    agirlikli_dizi = agirlikHesapla(siralanmis_mesafeler)
    # agirlik                uzaklık           sınıf
    #[0.613496932515337, 1.276714533480371, 'Iris-versicolor']
    return (siralanmis_mesafeler, agirlikli_dizi)

# verilerin içinden test sayısı kadar ornegi ayırır
def verileri_bol(veriler, test_sayisi):
   # def verileri_bol(veriler, test_sayisi):
    veriler_test = []
    for i in range(test_sayisi):
        rand_ = random.randint(0, int(len(veriler)-1))
        veriler_test.append(veriler[rand_])
        del veriler[rand_]
    return (veriler, veriler_test)

# bu veri setine ozel
def verileri_adil_bol(veriler, sinif_adi):
    veriler_test = []
    if(sinif_adi == 1):
        veriler_test = veriler[0:59]
        del veriler[0:59]
    elif(sinif_adi == 2):
        veriler_test = veriler[59:130]
        del veriler[59:130]
    elif(sinif_adi == 3):
        veriler_test = veriler[130:178]
        del veriler[130:178]
    return (veriler, veriler_test)

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
    
    print("\n*** Ağırlık toplamları ve Sınıf isimleri ***\n")
    print(a_toplam_dizi)
    print("-" * 50)
    print( "K Değeri : "+str(k_degeri) +" iken test verisinin sınıfı : " + str(sinif_degeri))

    return sinif_degeri



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
            
    print("\n****Sınıf Isim ve Sayilari Dizisi****\n")
    print(sinif_ve_eleman_sayilari)
    print("-" * 50)
    print( "K Değeri : "+str(k_degeri) + " iken test verisinin sınıfı : " + str(sinif_degeri))

    return sinif_degeri


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













