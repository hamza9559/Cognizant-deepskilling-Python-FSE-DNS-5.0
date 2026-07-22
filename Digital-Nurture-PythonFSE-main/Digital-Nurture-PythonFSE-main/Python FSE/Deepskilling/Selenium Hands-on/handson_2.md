# Hands-On 2: SDLC vs TDLC & Agile QA Integration

## Task 1: V-Model Mapping

### 9. V-Model ASCII Diagram Representation
                  V-MODEL INTEGRATION MATRIX
                  ==========================

   DEVELOPMENT PHASES (SDLC)              TESTING PHASES (TDLC)
   -------------------------              ---------------------

  [ Requirements Analysis ] -------------> [ Acceptance Testing ]
       \                                         /
        \                                       /
   [ System Architecture ] --------------> [ System Testing ]
         \                                     /
          \                                   /
     [ Module / Detail Design ] -------> [ Integration Testing ]
           \                                 /
            \                               /
             -----> [ Coding / Build ] <----
                     (Bottom Vertex)

### 10. Test Artifacts Map per Phase
*   **Requirements Design Phase:** The **Acceptance Test Plan** and User Story Acceptance Criteria definitions are generated here.
*   **Architecture Design Phase:** The **System Test Plan** along with comprehensive End-to-End Core Integration Test Scenario drafts are designed here.
*   **Module Design Phase:** Detailed **Integration Test Cases** and component API contract matching schemas are generated here.
*   **Coding Phase:** **Unit Test Scripts**, execution suites, and code coverage configuration profiles are authored alongside the application code.

### 11. Entry and Exit Criteria Matrix

| Testing Level | Entry Criteria | Exit Criteria |
| :--- | :--- | :--- |
| **Unit Testing** | • Source code compiles cleanly.<br>• Code review tool approvals achieved. | • 100% of unit test scripts run successfully.<br>• Minimum 80% statement coverage achieved. |
| **Integration Testing**| • Unit testing phase successfully closed.<br>• API modules are deployed to target environment. | • All structural interface data flows test successfully.<br>• 0 open critical integration path defects. |
| **System Testing** | • Integrated application build passes smoke check.<br>• Test environment configurations match prod baseline. | • 100% of active system tests executed.<br>• Defect burn down charts meet target shipping baseline. |
| **Acceptance Testing** | • System testing phase successfully closed.<br>• Deployment packages verified clean. | • Business stakeholders sign off on UAT metrics.<br>• System documentation meets release compliance. |

### 12. Two Early QA Engagement Points in the V-Model
1.  **Requirements Analysis Validation:** Participating directly in structural engineering requirements reviews. This catches ambiguities, logical conflicts, and non-testable clauses before they are passed down to architecture designers.
2.  **Architecture & Design Spec Review:** Analyzing structural interaction specifications early to identify system bottlenecks, missing edge cases, and API contract design issues before coding begins.

---

## Task 2: Agile QA and Shift-Left Testing

### 13. Three Traditional Waterfall Pitfalls for Course Management API
1.  **Late Defect Discovery:** System defects are found only at the end of the timeline. A core issue discovered here could require rewriting architecture code, risking project delays.
2.  **High Cost of Remediating Bugs:** A database schema mistake caught late costs significantly more to fix than if it had been resolved during early integration planning.
3.  **QA Compression Crunch:** If developer coding timelines slip, the testing timeline is often cut short to preserve the final release date, leading to insufficient test coverage.

### 14. QA Engineer Role in Agile Ceremonies
*   **Sprint Planning:** Helps define robust, testable Acceptance Criteria for user stories using Given-When-Then patterns, ensuring sizing calculations account for testing effort.
*   **Daily Standup:** Highlights testing progress, identifies blocking bugs, and aligns with developers to test completed items early in the cycle.
*   **Sprint Review:** Demonstrates functional verification stability, validating that the user stories delivered match the definition of done.
*   **Retrospective:** Analyzes recurring defect root causes and suggests improvements for code health, automation coverage, and team delivery velocity.

### 15. Shift-Left Practices Applied to Course Management API
*   **(a) Reviewing Requirements for Testability:** Inspecting the course creation rules early to ensure inputs like validation lengths and duplicate constraints are clearly defined before development starts.
*   **(b) Writing Test Cases Before Code (TDD/BDD):** Drafting functional test schemas alongside engineers before implementation, which helps clarify edge cases and minimizes downstream coding mistakes.
*   **(c) Static Code Analysis:** Setting up automated linting tools in the pipeline to flag syntax formatting errors, security vulnerabilities, and code complexity before code is merged.
*   **(d) API Contract Testing Before Integration:** Verifying request/response payloads against Swagger specifications early using mock endpoints, allowing frontend and backend development to proceed in parallel without integration delays.

### 16. Acceptance Criteria in Given-When-Then (Gherkin) Format
*   **Scenario 1: Happy Path Course Creation**
    *   **Given** the college administrator is authenticated and on the course creation portal
    *   **When** they submit a valid course payload containing code `"CS302"`, name `"Advanced Python"`, and credits `4`
    *   **Then** the system should successfully save the record and return an HTTP `201 Created` response.
*   **Scenario 2: Prevent Duplicate Course Code Entries**
    *   **Given** a course with the unique code `"CS302"` already exists in the system database
    *   **When** the administrator attempts to submit another course request using code `"CS302"`
    *   **Then** the system should reject the request, returning an error message stating `"Course code already exists"`.
*   **Scenario 3: Validation Check for Missing Required Attributes**
    *   **Given** the administrator initializes a course creation operation
    *   **When** they omit the mandatory course name field from the submission payload
    *   **Then** the system should block the request, returning an HTTP `400 Bad Request` with an explicit message identifying the missing field.