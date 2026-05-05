# Customer Workflow Standard Operating Procedure (SOP)
**Application:** Yoga Meditation App (Frappe/ERPNext)

This Standard Operating Procedure outlines the end-to-end customer journey and how it maps to the modules and DocTypes within the Yoga Meditation ERP system.

## Phase 1: Customer Onboarding & Profiling

### 1. Registration (`Student Member`)
When a new customer walks in or registers online, their profile is captured in the system.
* **Action:** Create a new **Student Member** document.
* **Key Data Captured:** Name, Mobile No, Email, Date of Birth, Health conditions, injuries, yoga experience level, and preferred instructor or yoga style.
* **Outcome:** An automated backend process links this Student Member to a standard ERPNext **Customer** (under the "Wellness Members" group) for billing purposes.

## Phase 2: Purchasing Memberships & Packages

### 2. Selecting a Package (`Wellness Package`)
Customers can choose to buy class bundles, monthly unlimited passes, or specific retreat packages.
* **Action:** The studio manager configures available **Wellness Packages** (e.g., "10 Class Pass", "Unlimited Monthly").
* **Customer Selection:** When the customer pays, their **Student Member** profile is updated with their active package, tracking their "Classes Purchased" and "Classes Remaining".

## Phase 3: Scheduling & Booking

### 3. Reviewing the Schedule (`Yoga Class` / `Meditation Session`)
The studio maintains a calendar of upcoming sessions.
* **Action:** Instructors or managers create **Yoga Class** or **Meditation Session** records with a specific Date, Start Time, Instructor, and Maximum Capacity.

### 4. Booking a Slot (`Booking`)
A customer reserves their spot for a scheduled class or session.
* **Action:** Create a **Booking** record.
* **Process:** Select the Student and Booking Type (Single Class, Meditation Session, or Wellness Package deduction). If paying out-of-pocket, the booking tracks payment status. If using a package, it deducts from their `Student Member` package balance.

## Phase 4: Class Execution & Attendance

### 5. Checking In (`Attendance Record`)
When the customer arrives at the studio for their booked class.
* **Action:** The instructor opens the **Attendance Record** for the specific Yoga Class or Meditation Session.
* **Process:** Mark the student as "Present". This confirms the booking was fulfilled and prevents no-show discrepancies.

## Phase 5: Tracking & Progression

### 6. Setting Goals (`Wellness Goal`)
For long-term students, instructors can set targeted wellness goals (e.g., "Master Headstand", "Lower Stress Levels").
* **Action:** Create a **Wellness Goal** linked to the Student Member. 
* **Process:** Define target completion dates and specific milestones.

### 7. Monitoring Progress (`Progress Tracker`)
Instructors track the student's journey over time to ensure they are getting value from the studio.
* **Action:** Add entries in the **Progress Tracker**.
* **Process:** Record physical measurements, flexibility improvements, mindfulness scores, and general instructor notes after key milestones or monthly check-ins.
