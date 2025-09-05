# 🛒 PHP MySQL Marketplace  

This is an **online marketplace platform** built using **PHP and MySQL**, where users can **buy and sell products** with ease. The project demonstrates the use of **PHP for server-side scripting** and **MySQL for database management**.  

![🛍 Marketplace Banner](./src/images/banner.png?raw=true)

---

## 🎯 **Features**  

✅ **🔐 User Registration & Login** – Users can create accounts, log in, and manage their profiles  
✅ **🛍 Product Listings** – Sellers can list products with price, description, and images  
✅ **🔎 Search & Filters** – Users can search for products and filter them based on various criteria  
✅ **🛒 Shopping Cart** – Users can add products to their cart and proceed to checkout  
✅ **📦 Order Management** – Admins can manage orders and update order statuses  

---

## 🔑 **Login Page** 
![🔑 Login Roles](./src/images/roles.png?raw=true)

- **🖥 Admin Login:** `serein`  
- **👤 Seller Login:** `seller`  
- **👤 User Login:** `user`  
- **🔑 Password:** `Fpt1409!@`  

---

## 👥 **User Roles**  
### 🏆 **Admin**  
![⚙ Admin Panel](./src/images/admin.png?raw=true)
- 🔹 Manages the entire marketplace  
- 🔹 Can view and datyuno1409/php-mysql-marketplace.git
```

### 2️⃣ **Navigate to the Project Directory**  
```bash
cd php-mysql-marketplace
```

### 3️⃣ **Set Up the Database**  
- **Create a new MySQL database**:  
  ```sql
  CREATE DATABASE marketplace;
  ```
- **Import the database schema**:  
  ```bash
  mysql -u yourusername -p marketplace < db/database.sql
  ```

### 4️⃣ **Configure Database Connection**  
- Open the **`config.php`** file in the root directory  
- Update the database credentials:  
  ```php
  <?php

  public function __construct() {
      $servername = "localhost";
      $username = "your_username";
      $password = "password";
      $dbname = "marketplace";

      $this->conn = new mysqli($servername, $username, $password, $dbname);

      if ($this->conn->connect_error) {
          die("Connection failed: " . $this->conn->connect_error);
      }
  }
  ```
- **Ensure you have a `Database` class** in the `config.php` file  

### 5️⃣ **Run the Application**  
- Deploy on a **PHP-compatible server** (Apache, Nginx, or XAMPP)  
- Open your browser and access:  
  ```
  http://localhost/php-mysql-marketplace
  ```

---


## 🖥 Technologies Used
![HTML](https://img.shields.io/badge/HTML-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-%23563D7C.svg?style=for-the-badge&logo=bootstrap&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-%23F7DF1C.svg?style=for-the-badge&logo=javascript&logoColor=black)
![jQuery](https://img.shields.io/badge/jQuery-%230e76a8.svg?style=for-the-badge&logo=jquery&logoColor=white)
![PHP](https://img.shields.io/badge/PHP-%23777BB4.svg?style=for-the-badge&logo=php&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-%234479A1.svg?style=for-the-badge&logo=mysql&logoColor=white)

## 📜 License
This project is open-source and available under the **MIT License**.

## 🤝 Contributing  
🎯 Contributions are welcome! If you have suggestions or want to enhance the project, feel free to fork the repository and submit a pull request.

## 📬 Connect with Me  
💬 I love meeting new people and discussing tech, business, and creative ideas. Let’s connect! You can reach me on these platforms:

<div align="center">
  <table>
    <tr>
      <td>
        <a href="https://iqbolshoh.uz" target="_blank">
          <img src="https://img.icons8.com/color/48/domain.png" 
               height="40" width="40" alt="Website" title="Website" />
        </a>
      </td>
      <td>
        <a href="mailto:iilhomjonov777@gmail.com" target="_blank">
          <img src="https://github.com/gayanvoice/github-active-users-monitor/blob/master/public/images/icons/gmail.svg"
               height="40" width="40" alt="Email" title="Email" />
        </a>
      </td>
      <td>
        <a href="https://github.com/serein" target="_blank">
          <img src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/github.svg"
               height="40" width="40" alt="GitHub" title="GitHub" />
        </a>
      </td>
      <td>
        <a href="https://www.linkedin.com/in/iqbolshoh/" target="_blank">
          <img src="https://github.com/gayanvoice/github-active-users-monitor/blob/master/public/images/icons/linkedin.svg"
               height="40" width="40" alt="LinkedIn" title="LinkedIn" />
        </a>
      </td>
      <td>
        <a href="https://t.me/iqbolshoh_777" target="_blank">
          <img src="https://github.com/gayanvoice/github-active-users-monitor/blob/master/public/images/icons/telegram.svg"
               height="40" width="40" alt="Telegram" title="Telegram" />
        </a>
      </td>
      <td>
        <a href="https://wa.me/998997799333" target="_blank">
          <img src="https://github.com/gayanvoice/github-active-users-monitor/blob/master/public/images/icons/whatsapp.svg"
               height="40" width="40" alt="WhatsApp" title="WhatsApp" />
        </a>
      </td>
      <td>
        <a href="https://instagram.com/iqbolshoh_777" target="_blank">
          <img src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/instagram.svg"
               height="40" width="40" alt="Instagram" title="Instagram" />
        </a>
      </td>
      <td>
        <a href="https://x.com/iqbolshoh_777" target="_blank">
          <img src="https://img.shields.io/badge/X-000000?style=for-the-badge&logo=x&logoColor=white"
               height="40" width="40" alt="X" title="X (Twitter)" />
        </a>
      </td>
      <td>
        <a href="https://www.youtube.com/@Iqbolshoh_777" target="_blank">
          <img src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/youtube.svg"
               height="40" width="40" alt="YouTube" title="YouTube" />
        </a>
      </td>
    </tr>
  </table>
</div>
