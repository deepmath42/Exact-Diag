# Bose–Hubbard Modeli – GUI Tabanlı Sayısal Simülasyon

Bu depo, **Bose–Hubbard modelinin** küçük sistemler için **tam diyagonalizasyon** yöntemiyle çözülmesini ve sonuçların **grafiksel kullanıcı arayüzü (GUI)** üzerinden incelenmesini sağlar.

Proje özellikle:
- Kuantum çoklu cisim sistemleri
- Hesaplamalı fizik
- Eğitim ve demonstrasyon amaçlı simülasyonlar

için tasarlanmıştır.

---

## 📌 Fiziksel Arka Plan

### Bose–Hubbard Hamiltonyeni

GitHub Markdown LaTeX render etmediği için Hamiltonyen **resim olarak** verilmiştir:

![Bose-Hubbard Hamiltonian](https://latex.codecogs.com/png.image?\dpi{120}\hat{H}=-t\sum_{\langle i,j \rangle}(b_i^\dagger b_j + b_j^\dagger b_i)+\frac{U}{2}\sum_i n_i(n_i-1)-\mu\sum_i n_i)

Burada:
- **t** : Hopping genliği  
- **U** : Yerinde etkileşim  
- **μ** : Kimyasal potansiyel  
- **nᵢ = bᵢ† bᵢ** : i. sitedeki bozon sayısı  
- **Periyodik sınır koşulları** uygulanmaktadır

---

## 🧮 Sayısal Yöntem

- Fock uzayı açıkça oluşturulur
- Hamiltonyen **sparse matris** (SciPy) olarak yazılır
- Temel durum enerjisi **Lanczos tabanlı eigsh** algoritması ile hesaplanır

### Beklenti Değeri (Yoğunluk)

Site başına parçacık yoğunluğu:

![Density Formula](https://latex.codecogs.com/png.image?\dpi{120}\langle n_i \rangle = \sum_{\alpha} |\psi_\alpha|^2 n_i^{(\alpha)})

ASCII gösterim:

```
<n_i> = Σ |ψ_α|² · n_i(α)
```

---

## 🧩 Özellikler

- 🔢 Otomatik Hilbert uzayı üretimi
- ⚙️ Sparse Hamiltonyen matrisi
- 🧮 Temel durum enerjisi hesabı
- 📊 Site başına yoğunluk dağılımı
- 🖥️ Tkinter tabanlı GUI
- 📁 Sonuçları **Excel (.xlsx)** formatında dışa aktarma
- 🧵 Thread tabanlı hesaplama (arayüz donmaz)

---

## 🚀 Kurulum

### Gereksinimler

Python 3.9+ önerilir.

```bash
pip install numpy scipy pandas
```

> Tkinter, Python ile birlikte varsayılan olarak gelir.

---

## ▶️ Çalıştırma

```bash
python bose_hubbard_gui.py
```

Adımlar:
1. Model parametrelerini girin
2. **Hesapla** butonuna basın
3. Sonuçları GUI üzerinden inceleyin
4. **Excel'e Kaydet** ile çıktıları dışa aktarın

---

## 🧪 Parametreler

| Parametre | Açıklama |
|---------|---------|
| t | Hopping genliği |
| U | Etkileşim şiddeti |
| μ | Kimyasal potansiyel |
| n_site | Lattice site sayısı |
| n_max | Site başına maksimum bozon |

⚠️ **Uyarı:** Hilbert uzayı boyutu:

![Hilbert Size](https://latex.codecogs.com/png.image?\dpi{120}(n_{max}+1)^{n_{site}})

şeklinde **üstel** büyür.

---

## 📤 Çıktılar

- Temel durum enerjisi
- Site başına yoğunluk dağılımı
- Ortalama yoğunluk
- Hilbert uzayı boyutu
- Excel dosyası:
  - `Parameters`
  - `Density`
  - `Summary`

---

## 📁 Önerilen Proje Yapısı

```text
bose-hubbard-gui/
│
├── bose_hubbard_gui.py
├── README.md
├── requirements.txt
└── docs/
    └── formulas.tex
```

📄 **Tüm matematiksel türetmeler** `docs/formulas.tex` dosyasında LaTeX formatında verilebilir.

---

## 🎓 Akademik Kullanım

Bu kod:
- Lisans ve yüksek lisans derslerinde
- Hesaplamalı fizik uygulamalarında
- Yapay sinir ağlarıyla Bose–Hubbard modeli karşılaştırmaları öncesinde

**referans tam diyagonalizasyon** aracı olarak kullanılabilir.

---

## 📚 Atıf

Bu yazılımı akademik çalışmanızda kullanırsanız aşağıdaki yayına atıf verebilirsiniz:

> Erdal, Ç. K., Atav, Ü. (2023). *Kuantum çoklu cisim probleminde yapay sinir ağları yönteminin kullanımı*. Fen Bilimleri ve Matematik Alanında Akademik Araştırma ve Derlemeler. DOI: 10.5281/zenodo.10060693

---

## 👤 Geliştirici

**Çağrı Kemal ERDAL**  
PhD – Fizik (Kuantum Çoklu Cisim Sistemleri)  
Hesaplamalı Fizik • Yapay Sinir Ağları • Eğitim Teknolojileri

📧 İletişim: kemalerdal@gmail.com

---

## 📝 Lisans

Bu proje eğitim ve akademik amaçlı kullanım için açıktır. Ticari kullanım için geliştiriciyle iletişime geçiniz.

