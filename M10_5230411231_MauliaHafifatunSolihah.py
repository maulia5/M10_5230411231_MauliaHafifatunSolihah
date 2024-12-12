import mysql.connector

# Koneksi ke MySQL
conn = mysql.connector.connect(
    user = "root",
    host = "localhost",
    password = "",
    database = "penjualan"
)

cur = conn.cursor()

# Membuat Tabel Pegawai
cur.execute("""CREATE TABLE Pegawai (
            NIK INT NOT NULL PRIMARY KEY,
            Nama_Pegawai VARCHAR(25),
            Alamat VARCHAR(255))""")

# Membuat Tabel Transaksi
cur.execute("""CREATE TABLE Transaksi (
            No_Transaksi CHAR(5) NOT NULL PRIMARY KEY,
            Detail_Transaksi VARCHAR(255),
            NIK INT)""")

# Membuat Tabel Produk
cur.execute("""CREATE TABLE Produk (
            Kode_Produk INT NOT NULL PRIMARY KEY,
            No_Transaksi CHAR(5),
            Nama_Produk VARCHAR(50),
            Jenis_Produk VARCHAR(50),
            Harga FLOAT(5, 3))""")

# Membuat Tabel Struk
cur.execute("""CREATE TABLE Struk ( 
            No_Struk CHAR (5),
            No_Transaksi CHAR(5),
            NIK INT,
            Nama_Pegawai VARCHAR(25),
            Kode_Produk INT(2),
            Nama_Produk VARCHAR(50),
            Total_Harga FLOAT(5, 3))""")

#Add foreign key
cur.execute("""ALTER TABLE Transaksi 
            ADD FOREIGN KEY (NIK) 
            REFERENCES Pegawai(NIK)""")

cur.execute("""ALTER TABLE Produk 
            ADD FOREIGN KEY (No_Transaksi) 
            REFERENCES Transaksi(No_Transaksi)""")

cur.execute("""ALTER TABLE Struk 
            ADD FOREIGN KEY (No_Transaksi) 
            REFERENCES Transaksi(No_Transaksi)""")

cur.execute("""ALTER TABLE Struk 
            ADD FOREIGN KEY (NIK) 
            REFERENCES Pegawai(NIK)""")

cur.execute("""ALTER TABLE Struk 
            ADD FOREIGN KEY (Kode_Produk) 
            REFERENCES Produk(Kode_Produk)""")

while True:
    print("\nPilih Menu:")
    print("1. Lihat Data")
    print("2. Input Data Pegawai")
    print("3. Input Data Transaksi")
    print("4. Input Data Produk")
    print("5. Pilih Produk")
    print("6. Cetak Struk")
    print("7. Ubah data")
    print("8. Hapus Struk")
    print("9. Keluar")

    pilihan = int(input("Masukkan pilihan (1-9): "))
    
    if pilihan == 1:
        # Melihat data pegawai
        cur.execute("SELECT * FROM Pegawai")
        print("\nData Pegawai:")
        for row in cur.fetchall():
            print(row)

        # Melihat data transaksi
        cur.execute("SELECT * FROM Transaksi")
        print("\nData Transaksi:")
        for row in cur.fetchall():
            print(row)

        # Melihat Data Produk
        cur.execute("SELECT * FROM Produk")
        print("\nData Produk:")
        for row in cur.fetchall():
            print(row)

        # Melihat data struk
        cur.execute("SELECT * FROM Struk")
        print("\nData Struk:")
        for row in cur.fetchall():
            print(row)

    elif pilihan == 2:
        # input data pegawai
        NIK = input("Masukkan NIK: ")
        Nama_Pegawai = input("Masukkan Nama Pegawai: ")
        Alamat = input("Masukkan Alamat: ")
        
        cur.execute("INSERT INTO Pegawai VALUES (%s, %s, %s)", (NIK, Nama_Pegawai, Alamat))
        conn.commit()
        print("Data pegawai berhasil ditambahkan.")

    elif pilihan == 3:
        # input data transaksi
        No_Transaksi = input("Masukkan No. Transaksi: ")
        Detail_Transaksi = input("Masukkan Detail Transaksi: ")
        NIK = input("Masukkan NIK: ")
        
        cur.execute("INSERT INTO Transaksi VALUES (%s, %s, %s)", (No_Transaksi, Detail_Transaksi, NIK))
        conn.commit()
        print("Data transaksi berhasil ditambahkan.")

    elif pilihan == 4:
        # input data produk
        Kode_Produk = input("Masukkan Kode Produk: ")
        No_Transaksi = input("Masukkan No. Transaksi: ")
        Nama_Produk = input("Masukkan Nama Produk: ")
        Jenis_Produk = input("Masukkan Jenis Produk: ")
        Harga = float(input("Masukkan Harga: "))
        
        cur.execute("INSERT INTO Produk VALUES (%s, %s, %s, %s, %s)", (Kode_Produk, No_Transaksi, Nama_Produk, Jenis_Produk, Harga))
        conn.commit()
        print("Data produk berhasil ditambahkan.")

    elif pilihan == 5:
        # Tampilkan semua produk 
        cur.execute("SELECT Kode_Produk, Nama_Produk, Jenis_Produk, Harga FROM Produk")
        produk = cur.fetchall()
        
        print("\nDaftar Produk:")
        for product in produk:
            print(f"Kode: {product[0]}, Nama: {product[1]}, Jenis: {product[2]}, Harga: Rp {product[3]:.3f}")
        
        pilihan_produk = input("Masukkan kode produk (atau 'exit'): ")
        if pilihan_produk.lower() == 'exit':
            continue
        
        # Validasi pilihan produk
        cur.execute("SELECT * FROM Produk WHERE Kode_Produk = %s", (pilihan_produk,))
        pilih_produk = cur.fetchone()
        if pilih_produk:
            print("\nProduk Terpilih:")
            print(f"Nama: {pilih_produk[2]}, Harga: Rp {pilih_produk[4]:.3f}")
        else:
            print("Produk tidak ditemukan.")

    elif pilihan == 6:
        # Cetak Struk 
        No_Transaksi = input("Masukkan No. Transaksi: ")

        # Ambil data transaksi
        cur.execute("""
            SELECT p.NIK, p.Nama_Pegawai, pr.Kode_Produk, pr.Nama_Produk, pr.Harga 
            FROM Transaksi t
            JOIN Pegawai p ON t.NIK = p.NIK
            JOIN Produk pr ON t.No_Transaksi = pr.No_Transaksi
            WHERE t.No_Transaksi = %s
        """, (No_Transaksi,))
        hasil = cur.fetchall()

        if not hasil:
            print("Transaksi tidak ditemukan atau tidak ada produk.")
        else:
            # Hitung total harga
            total_harga = sum(item[4] for item in hasil)

            # Nomor Struk
            No_Struk = f"ST{No_Transaksi}"

            # Cetak struk
            print("\n=== STRUK PEMBAYARAN ===")
            print(f"No. Struk    : {No_Struk}")
            print(f"No. Transaksi: {No_Transaksi}")
            print(f"Pegawai      : {hasil[0][1]}")
            print("-" * 40)
            print(f"{'Produk':<20}{'Harga':>12}")
            print("-" * 40)
            for item in hasil:
                print(f"{item[3]:<20}Rp {item[4]:>10,.3f}")
            print("-" * 40)
            print(f"{'TOTAL':<19} Rp {total_harga:>10,.3f}")
            print("=" * 40)

            # Memasukkan ke dalam tabel
            for item in hasil:
                cur.execute("""
                    INSERT INTO Struk (No_Struk, No_Transaksi, NIK, Nama_Pegawai, Kode_Produk, Nama_Produk, Total_Harga)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (No_Struk, No_Transaksi, item[0], item[1], item[2], item[3], total_harga))
            conn.commit()

    elif pilihan == 7:
        print("\nPilih jenis data yang ingin diubah:")
        print("1. Ubah Data Pegawai")
        print("2. Ubah Data Transaksi")
        print("3. Ubah Data Produk")
        
        pilih = int(input("Masukkan pilihan (1-3): "))
        
        if pilih == 1:
            # Ubah Data Pegawai
            NIK = input("Masukkan NIK pegawai yang ingin diubah: ")
            Nama_Pegawai = input("Masukkan Nama Pegawai Baru: ")
            Alamat = input("Masukkan Alamat Baru: ")
            
            cur.execute("""
                UPDATE Pegawai 
                SET Nama_Pegawai = %s, Alamat = %s
                WHERE NIK = %s
            """, (Nama_Pegawai, Alamat, NIK))
            conn.commit()
            print("Data pegawai berhasil diperbarui.")
            
        elif pilih == 2:
            # Ubah Data Transaksi
            No_Transaksi = input("Masukkan No. Transaksi yang ingin diubah: ")
            Detail_Transaksi = input("Masukkan Detail Transaksi Baru: ")
            
            cur.execute("""
                UPDATE Transaksi 
                SET Detail_Transaksi = %s
                WHERE No_Transaksi = %s
            """, (Detail_Transaksi, No_Transaksi))
            conn.commit()
            print("Data transaksi berhasil diperbarui.")
            
        elif pilih == 3:
            # Ubah Data Produk
            Kode_Produk = input("Masukkan Kode Produk yang ingin diubah: ")
            Nama_Produk = input("Masukkan Nama Produk Baru: ")
            Jenis_Produk = input("Masukkan Jenis Produk Baru: ")
            Harga = float(input("Masukkan Harga Baru: "))
            
            cur.execute("""
                UPDATE Produk 
                SET Nama_Produk = %s, Jenis_Produk = %s, Harga = %s
                WHERE Kode_Produk = %s
            """, (Nama_Produk, Jenis_Produk, Harga, Kode_Produk))
            conn.commit()
            print("Data produk berhasil diperbarui.")

        else:
            print("Pilihan tabel tidak valid.")
            break

    elif pilihan == 8:
        No_Struk = input("Masukkan No. Struk yang ingin dihapus: ")
        cur.execute("""DELETE FROM Struk WHERE No_Struk = %s""", (No_Struk,))
        conn.commit()
        print("Data struk berhasil dihapus.")

    elif pilihan == 9:
        break