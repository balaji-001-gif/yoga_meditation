# 🧘 Yoga & Meditation Management App for ERPNext v15+

A fully integrated Frappe/ERPNext application for managing yoga studios, meditation centers, and wellness businesses — inspired by [sarva.world](https://sarva.world).

---

## 📦 App Overview

| Property | Value |
|----------|-------|
| App Name | `yoga_meditation` |
| Framework | Frappe v15+ |
| ERP | ERPNext v15+ |
| Module | Yoga Meditation |
| License | MIT |

---

## 🗂️ Module Structure

```
yoga_meditation/
├── yoga_meditation/
│   ├── hooks.py                     # App hooks & events
│   ├── install.py                   # Post-install setup
│   ├── tasks.py                     # Scheduled tasks
│   ├── api.py                       # Whitelisted API endpoints
│   ├── module_def.json              # Module definition
│   │
│   ├── doctype/
│   │   ├── student_member/          # Student profiles & memberships
│   │   ├── instructor/              # Instructor profiles
│   │   ├── yoga_class/              # Yoga class scheduling
│   │   ├── class_enrollment/        # Child: Class student enrollment
│   │   ├── meditation_session/      # Meditation session management
│   │   ├── session_participant/     # Child: Session participants
│   │   ├── wellness_package/        # Membership packages & pricing
│   │   ├── package_inclusion/       # Child: Package inclusions
│   │   ├── booking/                 # Bookings (class / session / package)
│   │   ├── attendance_record/       # Attendance sheets
│   │   ├── attendance_student/      # Child: Per-student attendance
│   │   ├── wellness_goal/           # Student wellness goals
│   │   ├── goal_milestone/          # Child: Goal milestones
│   │   └── progress_tracker/        # Health & progress tracking
│   │
│   ├── report/
│   │   ├── student_progress_report/ # Individual student analytics
│   │   ├── class_attendance_report/ # Class-wise attendance
│   │   └── revenue_report/          # Monthly revenue analytics
│   │
│   ├── workspace/
│   │   └── yoga_meditation_hub/     # Main workspace
│   │
│   ├── notification/
│   │   ├── class_reminder_notification.json
│   │   ├── booking_confirmed_notification.json
│   │   ├── membership_expiry_notification.json
│   │   └── class_cancellation_notification.json
│   │
│   ├── email_template/
│   │   ├── booking_confirmation.json
│   │   ├── class_reminder.json
│   │   ├── class_confirmation.json
│   │   └── class_cancellation.json
│   │
│   ├── dashboard/
│   │   └── yoga_meditation_dashboard.json
│   │
│   ├── dashboard_chart/
│   │   ├── class_bookings_chart.json
│   │   ├── revenue_trend_chart.json
│   │   └── membership_status_chart.json
│   │
│   ├── fixtures/
│   │   └── roles.json               # Yoga Manager & Yoga Instructor roles
│   │
│   └── public/
│       └── js/
│           ├── yoga_class.js
│           ├── student_member.js
│           ├── booking.js
│           └── meditation_session.js
│
├── setup.py
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

## 🔑 Key DocTypes

### 👥 Student Member
- Auto-creates ERPNext Customer on creation
- Tracks membership status, classes remaining, health conditions
- Links to bookings, progress trackers, wellness goals

### 🧑‍🏫 Instructor
- Availability scheduling (days & time slots)
- Specializations via table multiselect
- Links to ERPNext Employee for payroll

### 🧘 Yoga Class (Submittable)
- Recurring class support (daily/weekly/bi-weekly/monthly)
- Auto-calculates available slots
- Instructor conflict detection
- Sends email notifications on submit/cancel

### 🪷 Meditation Session (Submittable)
- Audio guide & script attachment
- Participant feedback & ratings
- Online / In-studio / Outdoor / Hybrid modes

### 📦 Wellness Package
- Trial, Monthly, Quarterly, Annual, Drop-In
- GST support with ERPNext Tax Templates
- Discounted pricing

### 📝 Booking (Submittable)
- Single Class / Meditation Session / Wellness Package
- Auto-creates Sales Invoice on submit
- Auto-enrolls student in yoga class
- Sends email confirmation

### 📋 Attendance Record
- Auto-populates from Yoga Class or Meditation Session enrollments
- Updates student `classes_used` and `classes_remaining` after insert

### 🎯 Wellness Goal
- Auto-calculates progress percentage
- Marks as "Achieved" when 100% reached

### 📊 Progress Tracker
- Physical metrics: flexibility, strength, balance, endurance, weight, BMI
- Mental metrics: stress, mood, sleep quality, mindfulness
- Before/After progress photos

---

## 🧭 Customer Workflow SOP

This section outlines the end-to-end customer journey and how it maps to the modules and DocTypes within the Yoga Meditation ERP system.

### Phase 1: Customer Onboarding & Profiling
**1. Registration (`Student Member`)**
* **Action:** Create a new **Student Member** document.
* **Key Data Captured:** Name, Mobile No, Email, Date of Birth, Health conditions, injuries, yoga experience level, and preferred instructor or yoga style.
* **Outcome:** An automated backend process links this Student Member to a standard ERPNext **Customer** (under the "Wellness Members" group) for billing purposes.

### Phase 2: Purchasing Memberships & Packages
**2. Selecting a Package (`Wellness Package`)**
* **Action:** The studio manager configures available **Wellness Packages** (e.g., "10 Class Pass", "Unlimited Monthly").
* **Customer Selection:** When the customer pays, their **Student Member** profile is updated with their active package, tracking their "Classes Purchased" and "Classes Remaining".

### Phase 3: Scheduling & Booking
**3. Reviewing the Schedule (`Yoga Class` / `Meditation Session`)**
* **Action:** Instructors or managers create **Yoga Class** or **Meditation Session** records with a specific Date, Start Time, Instructor, and Maximum Capacity.

**4. Booking a Slot (`Booking`)**
* **Action:** Create a **Booking** record.
* **Process:** Select the Student and Booking Type (Single Class, Meditation Session, or Wellness Package deduction). If paying out-of-pocket, the booking tracks payment status. If using a package, it deducts from their `Student Member` package balance.

### Phase 4: Class Execution & Attendance
**5. Checking In (`Attendance Record`)**
* **Action:** The instructor opens the **Attendance Record** for the specific Yoga Class or Meditation Session.
* **Process:** Mark the student as "Present". This confirms the booking was fulfilled and prevents no-show discrepancies.

### Phase 5: Tracking & Progression
**6. Setting Goals (`Wellness Goal`)**
* **Action:** Create a **Wellness Goal** linked to the Student Member. 
* **Process:** Define target completion dates and specific milestones.

**7. Monitoring Progress (`Progress Tracker`)**
* **Action:** Add entries in the **Progress Tracker**.
* **Process:** Record physical measurements, flexibility improvements, mindfulness scores, and general instructor notes after key milestones or monthly check-ins.

---

## 🚀 Installation

### Prerequisites
- Frappe v15+
- ERPNext v15+
- Python 3.10+
- Node.js 18+

### Step 1: Get the App
```bash
cd ~/frappe-bench
bench get-app yoga_meditation /path/to/yoga_meditation
# or from git:
bench get-app yoga_meditation https://github.com/yourorg/yoga_meditation.git
```

### Step 2: Install on Site
```bash
bench --site your-site.localhost install-app yoga_meditation
```

### Step 3: Run Migrations
```bash
bench --site your-site.localhost migrate
```

### Step 4: Build Assets
```bash
bench build --app yoga_meditation
```

### Step 5: Restart
```bash
bench restart
```

---

## 🗂️ Git Repository Structure

```
yoga_meditation/           ← git root
├── .git/
├── .gitignore
├── setup.py
├── requirements.txt
├── pyproject.toml
├── README.md
└── yoga_meditation/       ← Python package
    ├── __init__.py
    ├── hooks.py
    ├── install.py
    ├── tasks.py
    ├── api.py
    ├── module_def.json
    └── yoga_meditation/   ← Module folder
        └── ...
```

### .gitignore
```
*.pyc
__pycache__/
*.egg-info/
node_modules/
dist/
.env
*.sqlite
```

---

## 🔧 Configuration After Install

### 1. Create Customer Group
Go to **Selling > Customer Group** → Create `Wellness Members`

### 2. Set Up Tax Templates
Go to **Accounting > Sales Taxes and Charges Template** → Create GST 18% template

### 3. Configure Email
Go to **Settings > Email Domain** → Set up outbound email for notifications

### 4. Assign Roles
- `Yoga Manager` — Full access to manage classes, students, packages
- `Yoga Instructor` — Read access + attendance marking

### 5. Set Up Workspace
The **Yoga & Meditation** workspace auto-appears in the desk after install.

---

## 📊 Reports

| Report | Type | Access |
|--------|------|--------|
| Student Progress Report | Script | Manager, Instructor |
| Class Attendance Report | Script | Manager, Instructor |
| Revenue Report | Script | Manager only |

---

## 🔔 Notifications

| Notification | Event | Trigger |
|--------------|-------|---------|
| Class Reminder | Days Before (1) | class_date on Yoga Class |
| Booking Confirmed | On New Submitted | Booking status = Confirmed |
| Membership Expiry | Days Before (7) | membership_end on Student |
| Class Cancellation | Value Change | status → Cancelled on Yoga Class |

---

## 🌐 API Endpoints

All endpoints are prefixed with `/api/method/yoga_meditation.yoga_meditation.api.`

| Method | Description |
|--------|-------------|
| `get_student_dashboard` | Student's bookings, goals, progress |
| `record_payment` | Mark booking as paid |
| `add_session_participant` | Add student to meditation session |
| `get_available_classes` | List available yoga classes by date |
| `quick_book` | Quick-enroll student in a class |
| `get_instructor_schedule` | Instructor's class schedule |

---

## 🔗 ERPNext Integrations

| ERPNext Module | Integration |
|----------------|-------------|
| **Customer** | Auto-created when Student Member is saved |
| **Sales Invoice** | Auto-created on Booking submit |
| **Employee** | Linked to Instructor for payroll |
| **Tax Template** | Used in Wellness Package pricing |

---

## 📅 Scheduled Tasks

| Task | Frequency | Description |
|------|-----------|-------------|
| `send_class_reminders` | Daily | Email reminders for next-day classes |
| `auto_mark_attendance` | Daily | Create attendance records for past classes |
| `generate_weekly_report` | Weekly | Log weekly summary |

---

## 🛠️ Development & Customization

### Adding a New DocType
```bash
bench new-doctype "Yoga Type" --module "Yoga Meditation"
```

### Running Tests
```bash
bench run-tests --app yoga_meditation
```

### Watching JS Changes
```bash
bench watch
```

---

## 📄 License

MIT License — free to use and modify.

---

*Built with ❤️ for the wellness community using Frappe Framework & ERPNext v15+*
