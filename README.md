# Loan Management System

A comprehensive web-based loan management system built with Flask and MongoDB that handles multiple types of loans including Gold Loans, Property Loans, and Automobile Loans. The system supports both customer and employee workflows with secure authentication and file upload capabilities.

## 🚀 Features

### Multi-Loan Support
- **Gold Loans**: Secure gold-based lending with document verification
- **Property Loans**: Real estate backed loans with property documentation
- **Automobile Loans**: Vehicle financing with RC and license verification

### User Management
- **Customer Portal**: Submit loan applications, track status, and manage offers
- **Employee Portal**: Review applications, send offers, and manage loan processing
- **Secure Authentication**: User registration and login with password hashing

### Core Functionality
- **Document Upload**: Support for PDF and image file uploads
- **Status Tracking**: Real-time loan application status updates
- **Offer Management**: Automated offer calculation and acceptance/rejection workflow
- **History Tracking**: Complete audit trail of all loan transactions
- **Notification System**: Real-time notifications for employees and customers

## 🛠️ Technology Stack

- **Backend**: Flask (Python web framework)
- **Database**: MongoDB (NoSQL database)
- **Authentication**: Werkzeug security for password hashing
- **File Handling**: Werkzeug utils for secure file uploads
- **Frontend**: HTML, CSS, JavaScript
- **Styling**: Custom CSS with modern UI components

## 📋 Prerequisites

Before running this application, make sure you have the following installed:

- Python 3.7 or higher
- MongoDB Atlas account (for cloud database)
- pip (Python package installer)

## 🔧 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Hackathon
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Database Configuration
The application uses MongoDB Atlas for data storage. Update the connection strings in `app.py` with your MongoDB credentials:

```python
# Update these connection strings with your MongoDB Atlas credentials
uri = "mongodb+srv://your_username:your_password@your_cluster.mongodb.net/"
```

### 4. Environment Setup
Create a secure secret key for the Flask application:
```python
# In app.py, update the secret key
app.secret_key = 'your_secure_secret_key_here'
```

### 5. Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 📁 Project Structure

```
Hackathon/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── static/                         # Static files
│   ├── css/                        # Stylesheets
│   │   ├── dashboard.css
│   │   ├── form.css
│   │   └── global.css
│   ├── uploads/                    # File uploads directory
│   └── style.css
└── templates/                      # HTML templates
    ├── dashboard.html              # Customer dashboard
    ├── employee_dashboard.html     # Employee dashboard
    ├── login.html                  # Login page
    ├── signup.html                 # Registration page
    ├── gold_loan_auth.html         # Gold loan form
    ├── property_loan_form.html     # Property loan form
    ├── automobile_loan_form.html   # Automobile loan form
    └── ...                         # Other template files
```

## 🔐 User Types & Workflows

### Customer Workflow
1. **Registration/Login**: Create account or sign in
2. **Loan Application**: Choose loan type and fill application form
3. **Document Upload**: Upload required documents (ID, property papers, etc.)
4. **Status Tracking**: Monitor application status
5. **Offer Management**: Review and accept/decline loan offers
6. **History**: View previous loan applications

### Employee Workflow
1. **Login**: Access employee portal
2. **Application Review**: View pending loan applications
3. **Document Verification**: Review uploaded documents
4. **Offer Generation**: Calculate and send loan offers
5. **Status Updates**: Update application status
6. **History Management**: Track completed applications

## 🏦 Loan Types & Requirements

### Gold Loan
- **Required Documents**: Government ID, Gold photos
- **Information**: Gold type, weight, purchase details
- **Bank Details**: Account information for disbursement
- **Offer Calculation**: Based on gold weight and current rates

### Property Loan
- **Required Documents**: Property documents, survey number
- **Information**: Property area, owner details
- **Offer Calculation**: Based on property area and market rates

### Automobile Loan
- **Required Documents**: RC book, driving license
- **Information**: Vehicle details, purchase year, value
- **Offer Calculation**: Based on vehicle value and depreciation

## 🔒 Security Features

- **Password Hashing**: Secure password storage using Werkzeug
- **Session Management**: Flask session-based authentication
- **File Upload Security**: Secure filename handling
- **Access Control**: Role-based access for customers and employees
- **Input Validation**: Form data validation and sanitization

## 📊 Database Collections

The application uses multiple MongoDB collections:
- `users`: User accounts and authentication
- `tickets`: Active loan applications
- `history`: Completed loan transactions
- `notifications`: System notifications

## 🚀 API Endpoints

### Authentication
- `GET/POST /login` - User login
- `GET/POST /signup` - User registration
- `GET /logout` - User logout

### Dashboard
- `GET /dashboard` - Main dashboard (redirects based on user type)
- `GET /employee_dashboard` - Employee dashboard
- `GET /customer_dashboard` - Customer dashboard

### Loan Management
- `GET/POST /gold_loan` - Gold loan application
- `GET/POST /property_loan` - Property loan application
- `GET/POST /automobile_loan` - Automobile loan application

### Ticket Management
- `POST /approve_ticket/<id>` - Approve loan application
- `POST /decline_ticket/<id>` - Decline loan application
- `POST /send_offer/<id>` - Send loan offer
- `POST /accept_offer/<id>` - Accept loan offer
- `POST /decline_offer/<id>` - Decline loan offer

## 🐛 Troubleshooting

### Common Issues

1. **MongoDB Connection Error**
   - Verify your MongoDB Atlas connection string
   - Check network connectivity
   - Ensure database credentials are correct

2. **File Upload Issues**
   - Ensure `static/uploads` directory exists
   - Check file permissions
   - Verify file size limits

3. **Authentication Problems**
   - Clear browser cookies and session data
   - Verify user credentials in database
   - Check Flask secret key configuration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- **Your Name** - *Initial work* - [YourGitHub](https://github.com/yourusername)

## 🙏 Acknowledgments

- Flask documentation and community
- MongoDB Atlas for database hosting
- Bootstrap for UI components inspiration

## 📞 Support

For support and questions, please contact:
- Email: your.email@example.com
- GitHub Issues: [Create an issue](https://github.com/yourusername/project/issues)

---

**Note**: This is a development version. For production deployment, ensure proper security measures, environment variables, and SSL certificates are configured. #   v i r t u s a - h a c k a t h o n - p r o j e c t  
 #   v i r t u s a - h a c k a t h o n - p r o j e c t  
 #   H a c k a t h o n - v i r t u s a  
 