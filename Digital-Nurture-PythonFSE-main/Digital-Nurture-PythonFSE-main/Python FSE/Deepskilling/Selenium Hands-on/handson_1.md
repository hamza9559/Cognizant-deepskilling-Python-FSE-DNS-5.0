# Hands-On 1: QA Concepts, Functional Testing & Defect Lifecycle

## Task 1: Map Testing Types to a Real System

### 1. Course Management API Test Cases by Level
*   **Unit Testing:** Tests the `calculate_course_duration(start_date, end_date)` utility function in pure isolation inside the business logic layer using mocked inputs. It ensures that the function computes the correct number of weeks without touching any database or HTTP framework components.
*   **Integration Testing:** Tests the interaction between the `POST /api/courses/` controller route logic and the underlying PostgreSQL/MySQL database layer. It verifies that when the endpoint handler invokes the data persistence layer, the course records are structurally written to the correct tables and database transaction constraints hold.
*   **System Testing:** Tests the full end-to-end operational flow of creating a course. The test fires an HTTP POST request to the API gateway, triggers authentication validation filters, processes the service layer validation rules, writes data to the database, logs the event to an audit system, and verifies the exact 201 Created JSON response footprint.
*   **User Acceptance Testing (UAT):** Performed from the perspective of a college administrator user profile. It validates a complete business workflow: an admin logs in, attempts to create a new "B.E. Computer Science and Engineering" course for the upcoming academic cohort, assigns faculty rules, and verifies if the user interface workflow strictly satisfies operational administrative requirements.

### 2. Classification: Functional vs. Non-Functional
*   **Functional Classification:** The Unit, Integration, System, and UAT test cases described above are all **Functional Testing** types because they evaluate *what* the system does against specified business requirements.
*   **Non-Functional Test Example:** 
    *   *Type:* Performance / Load Testing.
    *   *Scenario:* Evaluating how the `GET /api/courses/` endpoint handles concurrent volume. The target metrics mandate that the system must process 100 concurrent HTTP requests per second while keeping the 95th percentile latency below 200 milliseconds and maintaining a 0% request error rate.

### 3. Black-Box vs. White-Box Testing
*   **Black-Box Testing:** Testing software strictly from an external perspective without any internal knowledge of its foundational code structure, implementation algorithms, or internal paths. The tester interacts purely with the inputs and outputs of the software interfaces. This is typically performed by a **QA Tester**.
*   **White-Box Testing:** Testing software with full visibility and active structural verification of the inner program logic, statement branches, control flows, loops, and data paths. This is typically performed by a **Software Developer** during unit testing and early code reviews.

### 4. Formal Test Cases for POST /api/courses/ Endpoint

| Test Case ID | Description | Preconditions | Test Steps | Expected Result | Actual Result | Pass/Fail |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC_API_001** | Verify successful course creation with all valid payload inputs. | Admin user is authenticated; authentication bearer token is valid. | 1. Send POST request to `/api/courses/` with body: `{"code": "CS302", "name": "Advanced Python", "credits": 4}`.<br>2. Inspect HTTP status code.<br>3. Verify response body JSON structure. | 1. Status code is `201 Created`.<br>2. Response body contains a generated `course_id` and echoes matching metadata values. | | |
| **TC_API_002** | Verify validation error payload when submitting a duplicate course code. | A course with the code `"CS302"` already exists in the system database records. | 1. Send POST request to `/api/courses/` with body: `{"code": "CS302", "name": "Core Java & OOP", "credits": 3}`.<br>2. Inspect HTTP status code.<br>3. Verify error error message context. | 1. Status code is `400 Bad Request` or `409 Conflict`.<br>2. Response body provides a clear validation message: `"Course code already exists"`. | | |
| **TC_API_003** | Verify validation block when a mandatory field is missing from payload. | Admin user is authenticated; authentication bearer token is valid. | 1. Send POST request to `/api/courses/` with body: `{"name": "SQL Database Basics", "credits": 3}` *(Missing code field)*.<br>2. Inspect HTTP status code.<br>3. Observe validation response. | 1. Status code is `400 Bad Request`.<br>2. Response body explicitly isolates the missing element error: `"Course code is a required field"`. | | |

---

## Task 2: Defect Lifecycle & Severity Classification

### 5. Defect Lifecycle Description
The lifecycle tracking of a software defect moves sequentially through the following workflow states:
*   **New:** The defect is initially submitted and logged by the QA engineer.
*   **Assigned:** The test lead or project manager reviews the defect and routes it to a specific developer for mitigation.
*   **Open:** The developer changes the status to actively analyze the root cause and write a fix.
*   **Fixed:** The developer completes the code changes and deploys the remediation to the test environment.
*   **Retest:** The QA engineer executes the original steps to reproduce along with related regression steps.
*   **Verified:** The QA engineer confirms the problem no longer manifests under testing.
*   **Closed:** The defect is permanently archived out of active workflows.

**Alternative Workflow Branches:**
*   **Rejected:** The developer or lead changes the state to Rejected if the behavior is determined to match intended requirements, is a duplicate entry, or is unable to be reproduced due to invalid environment configurations.
*   **Deferred:** The defect is moved to Deferred if it is validated as a bug but scheduled to be fixed in a future release cycle due to low priority or tight shipping timelines.

### 6. Bug Classification & Justifications
*   **a) POST /api/courses/ returns 500 Internal Server Error for all requests.**
    *   *Severity:* Critical | *Priority:* P1 (Urgent)
    *   *Justification:* The core business feature of the application is completely broken, blocking all data entry. It represents a total system failure with no operational workaround.
*   **b) Course names longer than 150 characters are silently truncated without an error.**
    *   *Severity:* Medium | *Priority:* P3 (Normal)
    *   *Justification:* It causes silent data corruption in the database records, but the system remains online and operational for standard day-to-day strings.
*   **c) The /docs Swagger page has a typo in the API description.**
    *   *Severity:* Low | *Priority:* P4 (Low)
    *   *Justification:* It is a purely cosmetic presentation issue that does not degrade system processing calculations or technical reliability.
*   **d) Login with correct credentials occasionally returns 401 on the first attempt (intermittent).**
    *   *Severity:* High | *Priority:* P2 (High)
    *   *Justification:* Intermittent authentication failures indicate core system stability or race-condition problems inside session validation management. It disrupts user confidence and must be investigated promptly.

### 7. Defect Report for Bug (a)
*   **Defect ID:** DEF-CS-001
*   **Title:** HTTP 500 Internal Server Error thrown globally on POST /api/courses/ endpoint execution
*   **Environment:** QA-Staging Environment v2
*   **Build Version:** b5.0.14-rc1
*   **Severity:** Critical
*   **Priority:** P1
*   **Steps to Reproduce:**
    1. Open an API client (e.g., Postman) or command terminal.
    2. Set request headers: `Content-Type: application/json` and `Authorization: Bearer <valid_token>`.
    3. Construct a standard valid JSON body: `{"code": "CS101", "name": "Introduction to Python", "credits": 3}`.
    4. Execute the POST request to endpoint URL: `https://qa.api.coursemanagement.local/api/courses/`.
*   **Expected Result:** The endpoint creates the resource record, returning an HTTP status code `201 Created` along with the matching course record data payload.
*   **Actual Result:** The request fails instantly, returning an HTTP status code `500 Internal Server Error` with a generic stack trace body object.
*   **Attachments:** See attached `screenshot_of_500_error.png` showing the Postman client execution logs.

### 8. Difference Between Severity and Priority
*   **Severity:** Reflects the technical impact of a defect on the functional operation of the application. It answers: *How badly is the system broken?*
*   **Priority:** Reflects the business urgency of fixing a defect. It answers: *How fast do we need to patch this behavior?*
*   **Real-World Example (High Severity, Low Priority):** A critical memory leak or fatal crash occurs in a legacy component that is completely hidden behind a feature flag and scheduled to be fully removed from the system in the next month. The technical impact is extreme (High Severity), but because standard production users cannot execute the code path, the urgency to fix it is minimal (Low Priority).