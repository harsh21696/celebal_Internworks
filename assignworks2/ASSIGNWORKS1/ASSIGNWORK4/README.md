# Azure Cloud Fundamentals and Data Pipeline using Azure Data Factory
## Overview

This assignment demonstrates the implementation of an end-to-end data pipeline using **Microsoft Azure** services. The project utilizes **Azure Storage Account**, **Azure Blob Storage**, and **Azure Data Factory (ADF)** to validate metadata and copy a CSV dataset from a source location to a destination location.

---

## Objective

- Explore Azure Portal and Azure Cloud services.
- Create Azure Storage Account and Blob Container.
- Upload a CSV dataset.
- Configure Azure Data Factory.
- Create Linked Services and Datasets.
- Validate source file metadata.
- Build and execute a Copy Data pipeline.
- Verify successful data transfer.

---

## Technologies & Services Used

- Microsoft Azure
- Azure Resource Group
- Azure Storage Account
- Azure Blob Storage
- Azure Data Factory (ADF)
- Linked Service
- Source Dataset
- Destination Dataset
- Get Metadata Activity
- Copy Data Activity

---

## Folder Structure

```
ASSIGNWORKS4/
│
├── Azure_ADF_Assignment_Submission.docx
├── README.md
```

---

## Pipeline Workflow

```text
Sample - Superstore.csv
        │
        ▼
 Azure Blob Storage
        │
        ▼
 Source Dataset
        │
        ▼
 Get Metadata Activity
        │
        ▼
 Copy Data Activity
        │
        ▼
 Destination Dataset
        │
        ▼
 output.csv
```

---

## Tasks Performed

### Task 1 – Azure Portal
- Created Azure Resource Group.
- Explored Azure Portal.

### Task 2 – Storage Setup
- Created Azure Storage Account.
- Created Blob Container.
- Uploaded **Sample - Superstore.csv**.

### Task 3 – Azure Data Factory
- Created Azure Data Factory.
- Configured Azure Blob Storage Linked Service.
- Created Source and Destination Datasets.
- Implemented Get Metadata Activity.

### Task 4 – Pipeline Development
- Built Copy Data Pipeline.
- Connected Source and Destination Datasets.
- Configured Metadata Validation.

### Task 5 – Pipeline Execution
- Successfully executed the pipeline.
- Verified successful copy of the dataset.

### Task 6 – IAM Roles
- Assigned required Azure roles (Reader and Contributor).
- Verified Storage access from Azure Data Factory.

---

## Expected Output

- ✅ Metadata retrieved successfully.
- ✅ Source CSV validated.
- ✅ Data copied successfully.
- ✅ Output CSV created in Blob Storage.
- ✅ Pipeline executed successfully.

---

## Deliverables

- Resource Group Screenshot
- Storage Account Screenshot
- Blob Container Screenshot
- Linked Service Screenshot
- Source Dataset Screenshot
- Destination Dataset Screenshot
- Get Metadata Activity Screenshot
- Pipeline Design Screenshot
- Successful Pipeline Execution Screenshot
- IAM Role Assignment Screenshot

---

## Key Learnings

- Azure Resource Management
- Azure Blob Storage
- Azure Data Factory
- Linked Services
- Datasets
- Metadata Validation
- Copy Data Activity
- Pipeline Monitoring
- Azure IAM

---

**Harsh Wardhan**

**Internship:** Celebal Technologies – Data Engineering Internship

**Week:** 4 – Azure Cloud Fundamentals & Azure Data Factory