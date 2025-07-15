import os
import numpy as np
from flask import Flask, request, render_template, redirect, url_for
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename

app = Flask(__name__)
application = app
app.config['UPLOAD_FOLDER'] = 'static/uploaded'

# Load model
model = load_model('model/best_model.h5')

# Daftar kelas dan solusi
class_names = ['ea', 'healthy', 'leaf curl', 'leaf spot', 'whitefly', 'yellowish', 'another_class']

solusi_dict = {
    'healthy': (
        "Daun cabai dalam kondisi sehat dan tidak menunjukkan gejala penyakit. "
        "Pertahankan kebersihan lahan, rotasi tanaman, dan penyiraman yang konsisten untuk mencegah timbulnya penyakit. "
        "Lanjutkan pemantauan rutin serta pemberian nutrisi seimbang guna memastikan pertumbuhan optimal tanaman."
    ),

    'leaf curl': (
        "Gejala ini umumnya disebabkan oleh infeksi virus seperti Tomato Leaf Curl Virus (ToLCV) yang disebarkan oleh vektor kutu kebul. "
        "Lakukan pengendalian vektor dengan insektisida sistemik berbahan aktif imidakloprid atau gunakan perangkap kuning. "
        "Singkirkan tanaman yang terinfeksi berat untuk mencegah penyebaran lebih lanjut, dan gunakan varietas tahan virus jika tersedia."
    ),

    'leaf spot': (
        "Penyakit bercak daun biasanya disebabkan oleh infeksi jamur seperti Cercospora capsici atau bakteri seperti Xanthomonas. "
        "Perbaiki sirkulasi udara dengan menjarangkan tanaman, hindari penyiraman dari atas daun, dan gunakan fungisida seperti klorotalonil atau mankozeb secara teratur. "
        "Penting juga untuk membersihkan gulma di sekitar tanaman dan membuang daun yang terinfeksi."
    ),

    'whitefly': (
        "Kehadiran whitefly (kutu kebul) bisa menjadi vektor berbagai virus tanaman dan menyebabkan kerusakan fisik pada daun. "
        "Gunakan metode pengendalian terpadu seperti pemasangan perangkap kuning lengket, penyemprotan insektisida berbahan aktif abamektin atau neem oil, "
        "dan tanam tanaman penghalang seperti jagung di sekitar lahan untuk mengurangi invasi. "
        "Pantau populasi whitefly secara berkala agar tidak berkembang menjadi infestasi berat."
    ),
 
    'yellowish': (    
        "Daun menguning dapat disebabkan oleh defisiensi nitrogen atau ketidakseimbangan nutrisi lainnya seperti magnesium dan zat besi. "
        "Perbaiki kesuburan tanah dengan pemberian pupuk berimbang yang mengandung NPK dan unsur mikro. "
        "Lakukan pengukuran pH tanah dan sesuaikan jika terlalu asam atau basa. "
        "Gunakan kompos atau pupuk organik sebagai penambah bahan organik dan tingkatkan aktivitas mikroba tanah untuk membantu penyerapan nutrisi."
    ), 

    'another_class': (
        "Tanaman menunjukkan gejala tidak spesifik yang memerlukan observasi lebih lanjut. "
        "Disarankan untuk mengisolasi tanaman dari yang sehat, melakukan pemeriksaan terhadap gejala lainnya seperti perubahan batang atau buah, "
        "dan konsultasi dengan ahli pertanian atau penyuluh lapangan. "
        "Dokumentasikan perkembangan gejala dan pertimbangkan penggunaan teknologi citra multispektral jika tersedia untuk analisis lanjutan."
    )
}


def predict_image(path):
    img = image.load_img(path, target_size=(150, 150))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    pred = model.predict(img_array)
    class_idx = np.argmax(pred)

    if class_idx >= len(class_names):
        return "Kelas tidak diketahui", "Solusi tidak tersedia"

    kelas = class_names[class_idx]
    solusi = solusi_dict.get(kelas, "Solusi belum tersedia")
    return kelas, solusi

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/identifikasi', methods=['GET', 'POST'])
def identifikasi():
    if request.method == 'POST':
        file = request.files['gambar']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            kelas, solusi = predict_image(filepath)
            return render_template('hasil.html', filename=filename, kelas=kelas, solusi=solusi)
    return render_template('identifikasi.html')

@app.route('/cara-penggunaan')
def cara_penggunaan():
    return render_template('cara_penggunaan.html')

@app.route('/tentang')
def tentang():
    return render_template('tentang.html')

if __name__ == '__main__':
    app.run(debug=True)

# import os
# import numpy as np
# from flask import Flask, request, render_template, redirect, url_for
# from tensorflow.keras.models import load_model
# from tensorflow.keras.preprocessing import image
# from werkzeug.utils import secure_filename

# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = 'static/uploaded'

# # Load model
# # Pastikan jalur model benar relatif terhadap root aplikasi di cPanel
# model = load_model('model/best_model.h5')

# # Daftar kelas dan solusi
# class_names = ['ea', 'healthy', 'leaf curl', 'leaf spot', 'whitefly', 'yellowish', 'another_class']

# solusi_dict = {
#     'healthy': (
#         "Daun cabai dalam kondisi sehat dan tidak menunjukkan gejala penyakit. "
#         "Pertahankan kebersihan lahan, rotasi tanaman, dan penyiraman yang konsisten untuk mencegah timbulnya penyakit. "
#         "Lanjutkan pemantauan rutin serta pemberian nutrisi seimbang guna memastikan pertumbuhan optimal tanaman."
#     ),

#     'leaf curl': (
#         "Gejala ini umumnya disebabkan oleh infeksi virus seperti Tomato Leaf Curl Virus (ToLCV) yang disebarkan oleh vektor kutu kebul. "
#         "Lakukan pengendalian vektor dengan insektisida sistemik berbahan aktif imidakloprid atau gunakan perangkap kuning. "
#         "Singkirkan tanaman yang terinfeksi berat untuk mencegah penyebaran lebih lanjut, dan gunakan varietas tahan virus jika tersedia."
#     ),

#     'leaf spot': (
#         "Penyakit bercak daun biasanya disebabkan oleh infeksi jamur seperti Cercospora capsici atau bakteri seperti Xanthomonas. "
#         "Perbaiki sirkulasi udara dengan menjarangkan tanaman, hindari penyiraman dari atas daun, dan gunakan fungisida seperti klorotalonil atau mankozeb secara teratur. "
#         "Penting juga untuk membersihkan gulma di sekitar tanaman dan membuang daun yang terinfeksi."
#     ),

#     'whitefly': (
#         "Kehadiran whitefly (kutu kebul) bisa menjadi vektor berbagai virus tanaman dan menyebabkan kerusakan fisik pada daun. "
#         "Gunakan metode pengendalian terpadu seperti pemasangan perangkap kuning lengket, penyemprotan insektisida berbahan aktif abamektin atau neem oil, "
#         "dan tanam tanaman penghalang seperti jagung di sekitar lahan untuk mengurangi invasi. "
#         "Pantau populasi whitefly secara berkala agar tidak berkembang menjadi infestasi berat."
#     ),

#     'yellowish': (
#         "Daun menguning dapat disebabkan oleh defisiensi nitrogen atau ketidakseimbangan nutrisi lainnya seperti magnesium dan zat besi. "
#         "Perbaiki kesuburan tanah dengan pemberian pupuk berimbang yang mengandung NPK dan unsur mikro. "
#         "Lakukan pengukuran pH tanah dan sesuaikan jika terlalu asam atau basa. "
#         "Gunakan kompos atau pupuk organik sebagai penambah bahan organik dan tingkatkan aktivitas mikroba tanah untuk membantu penyerapan nutrisi."
#     ),

#     'another_class': (
#         "Tanaman menunjukkan gejala tidak spesifik yang memerlukan observasi lebih lanjut. "
#         "Disarankan untuk mengisolasi tanaman dari yang sehat, melakukan pemeriksaan terhadap gejala lainnya seperti perubahan batang atau buah, "
#         "dan konsultasi dengan ahli pertanian atau penyuluh lapangan. "
#         "Dokumentasikan perkembangan gejala dan pertimbangkan penggunaan teknologi citra multispektral jika tersedia untuk analisis lanjutan."
#     )
# }


# def predict_image(path):
#     img = image.load_img(path, target_size=(150, 150))
#     img_array = image.img_to_array(img) / 255.0
#     img_array = np.expand_dims(img_array, axis=0)

#     pred = model.predict(img_array)
#     class_idx = np.argmax(pred)

#     if class_idx >= len(class_names):
#         return "Kelas tidak diketahui", "Solusi tidak tersedia"

#     kelas = class_names[class_idx]
#     solusi = solusi_dict.get(kelas, "Solusi belum tersedia")
#     return kelas, solusi

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/identifikasi', methods=['GET', 'POST'])
# def identifikasi():
#     if request.method == 'POST':
#         # Pastikan 'gambar' ada di request.files sebelum mengaksesnya
#         if 'gambar' not in request.files:
#             # Handle case where no file part is in the request
#             return "Tidak ada file gambar yang diunggah.", 400
        
#         file = request.files['gambar']
        
#         # Jika pengguna tidak memilih file, browser mungkin mengirimkan bagian file kosong
#         if file.filename == '':
#             return "Tidak ada file yang dipilih.", 400

#         if file:
#             filename = secure_filename(file.filename)
#             # Pastikan folder 'static/uploaded' ada dan memiliki izin tulis
#             filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(filepath)

#             kelas, solusi = predict_image(filepath)
#             return render_template('hasil.html', filename=filename, kelas=kelas, solusi=solusi)
#     return render_template('identifikasi.html')

# @app.route('/cara-penggunaan')
# def cara_penggunaan():
#     return render_template('cara_penggunaan.html')

# @app.route('/tentang')
# def tentang():
#     return render_template('tentang.html')

# Baris di bawah ini dikomentari atau dihapus untuk deployment produksi di cPanel
# Flask akan dijalankan oleh WSGI server (misalnya Passenger) yang dikonfigurasi di cPanel
# if __name__ == '__main__':
#     app.run(debug=True)
