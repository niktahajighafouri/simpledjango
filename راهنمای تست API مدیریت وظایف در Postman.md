# راهنمای تست API مدیریت وظایف در Postman

این راهنما شامل مثال‌هایی از کوئری‌ها و میوتیشن‌های مختلف برای تست بخش مدیریت وظایف پروژه شما در Postman است.

**نکات مهم قبل از شروع تست در Postman:**

1.  **احراز هویت (Authentication):** تمام این عملیات نیاز به احراز هویت دارند. شما باید ابتدا با یک کاربر (مثلاً مدیر یا کاربر عادی) از طریق میوتیشن `tokenAuth` لاگین کرده و توکن JWT دریافت کنید. سپس این توکن را در هدر هر درخواست به صورت زیر ارسال کنید:
    *   `Key`: `Authorization`
    *   `Value`: `Bearer <YOUR_JWT_TOKEN_HERE>`

2.  **نوع درخواست (Request Type):**
    *   برای **کوئری‌ها (Queries)** و **میوتیشن‌هایی که فایل آپلود ندارند (Mutations without file upload)**، می‌توانید از حالت GraphQL در Postman استفاده کنید (Body -> GraphQL) و کوئری/میوتیشن را در بخش Query و متغیرها را در بخش GraphQL Variables وارد کنید.
    *   یا می‌توانید از درخواست `POST` با Body از نوع `raw` و `JSON (application/json)` استفاده کنید و ساختار زیر را ارسال نمایید:
        ```json
        {
            "query": "... your GraphQL query or mutation string ...",
            "variables": { ... your variables ... }
        }
        ```

3.  **شناسه‌ها (IDs):** در مثال‌های زیر، شناسه‌هایی مانند `task_id` یا `user_id` به صورت نمونه آورده شده‌اند. شما باید آن‌ها را با شناسه‌های واقعی موجود در سیستم خود جایگزین کنید (شناسه‌ها معمولاً رشته‌های Base64 کد شده هستند، مانند `"VGFza1R5cGU6MQ=="`).

4.  **نقش کاربران:** برای تست کامل دسترسی‌ها، با کاربران مختلف که به گروه‌های `Managers` و `Users` اختصاص داده شده‌اند، تست‌ها را انجام دهید.

---

## مثال‌های میوتیشن (Mutations)

### 1. ایجاد یک وظیفه جدید (CreateTask)
*   **توضیح:** این میوتیشن یک وظیفه جدید ایجاد می‌کند. فقط کاربرانی که در گروه `Managers` هستند می‌توانند این کار را انجام دهند.
*   **میوتیشن:**
    ```graphql
    mutation CreateNewTask($input: TaskInput!) {
      createTask(input: $input) {
        ok
        task {
          id
          title
          description
          dueDate
          status
          priority
          assignedTo {
            id
            username
          }
          createdBy {
            id
            username
          }
          createdAt
        }
      }
    }
    ```
*   **متغیرها (Variables):** (فرض کنید User ID با شناسه `"VXNlclR5cGU6MQ=="` وجود دارد)
    ```json
    {
      "input": {
        "title": "طراحی صفحه اصلی وبسایت",
        "description": "طراحی کامل UI/UX برای صفحه اصلی با در نظر گرفتن ریسپانسیو بودن.",
        "dueDate": "2025-06-15",
        "status": "TODO",
        "priority": "HIGH",
        "assignedToId": "VXNlclR5cGU6MQ==" 
      }
    }
    ```

### 2. به‌روزرسانی یک وظیفه (UpdateTask)
*   **توضیح:** این میوتیشن یک وظیفه موجود را به‌روزرسانی می‌کند. مدیران می‌توانند تمام فیلدها را تغییر دهند. کاربر ایجادکننده یا اختصاص‌داده‌شده فقط می‌تواند فیلدهای مشخصی (مثلاً `status` و `description`) را تغییر دهد.
*   **میوتیشن:**
    ```graphql
    mutation UpdateExistingTask($id: ID!, $input: UpdateTaskInput!) {
      updateTask(id: $id, input: $input) {
        ok
        task {
          id
          title
          description
          status
          priority
          dueDate
          assignedTo {
            username
          }
        }
      }
    }
    ```
*   **متغیرها (Variables):** (فرض کنید Task ID برابر `"VGFza1R5cGU6MQ=="` است)
    *   *مثال برای مدیر (تغییر همه چیز):*
        ```json
        {
          "id": "VGFza1R5cGU6MQ==",
          "input": {
            "title": "(اصلاح شده) طراحی صفحه اصلی وبسایت",
            "status": "IN_PROGRESS",
            "priority": "HIGH",
            "assignedToId": "VXNlclR5cGU6Mg==" 
          }
        }
        ```
    *   *مثال برای کاربر اختصاص‌داده‌شده (فقط تغییر وضعیت و توضیحات):*
        ```json
        {
          "id": "VGFza1R5cGU6MQ==",
          "input": {
            "status": "DONE",
            "description": "کار طراحی صفحه اصلی به اتمام رسید و فایل‌ها تحویل داده شد."
          }
        }
        ```

### 3. حذف یک وظیفه (DeleteTask)
*   **توضیح:** این میوتیشن یک وظیفه را حذف می‌کند. فقط کاربران گروه `Managers` می‌توانند این کار را انجام دهند.
*   **میوتیشن:**
    ```graphql
    mutation RemoveTask($id: ID!) {
      deleteTask(id: $id) {
        ok
        message
      }
    }
    ```
*   **متغیرها (Variables):** (فرض کنید Task ID برابر `"VGFza1R5cGU6MQ=="` است)
    ```json
    {
      "id": "VGFza1R5cGU6MQ=="
    }
    ```

### 4. ایجاد یک زیروظیفه جدید (CreateSubTask)
*   **توضیح:** این میوتیشن یک زیروظیفه برای یک وظیفه موجود ایجاد می‌کند. مدیران، ایجادکننده وظیفه مادر، یا کاربر اختصاص‌داده‌شده به وظیفه مادر می‌توانند این کار را انجام دهند.
*   **میوتیشن:**
    ```graphql
    mutation AddNewSubTask($input: SubTaskInput!) {
      createSubTask(input: $input) {
        ok
        subTask {
          id
          title
          description
          status
          task {
            id
            title
          }
        }
      }
    }
    ```
*   **متغیرها (Variables):** (فرض کنید Task ID مادر برابر `"VGFza1R5cGU6Mg=="` است)
    ```json
    {
      "input": {
        "taskId": "VGFza1R5cGU6Mg==",
        "title": "آماده‌سازی آیکون‌ها",
        "description": "طراحی و آماده‌سازی مجموعه آیکون‌های مورد نیاز برای صفحه اصلی.",
        "status": "TODO"
      }
    }
    ```

### 5. به‌روزرسانی یک زیروظیفه (UpdateSubTask)
*   **توضیح:** این میوتیشن یک زیروظیفه موجود را به‌روزرسانی می‌کند. دسترسی مشابه ایجاد زیروظیفه است.
*   **میوتیشن:**
    ```graphql
    mutation UpdateExistingSubTask($id: ID!, $input: UpdateSubTaskInput!) {
      updateSubTask(id: $id, input: $input) {
        ok
        subTask {
          id
          title
          description
          status
        }
      }
    }
    ```
*   **متغیرها (Variables):** (فرض کنید SubTask ID برابر `"U3ViVGFza1R5cGU6MQ=="` است)
    ```json
    {
      "id": "U3ViVGFza1R5cGU6MQ==",
      "input": {
        "title": "(اصلاح شده) آماده‌سازی آیکون‌ها وکتور",
        "status": "IN_PROGRESS"
      }
    }
    ```

### 6. حذف یک زیروظیفه (DeleteSubTask)
*   **توضیح:** این میوتیشن یک زیروظیفه را حذف می‌کند. دسترسی مشابه ایجاد زیروظیفه است.
*   **میوتیشن:**
    ```graphql
    mutation RemoveSubTask($id: ID!) {
      deleteSubTask(id: $id) {
        ok
        message
      }
    }
    ```
*   **متغیرها (Variables):** (فرض کنید SubTask ID برابر `"U3ViVGFza1R5cGU6MQ=="` است)
    ```json
    {
      "id": "U3ViVGFza1R5cGU6MQ=="
    }
    ```

---

## مثال‌های کوئری (Queries)

### 1. دریافت لیست تمام وظایف (AllTasks)
*   **توضیح:** مدیران تمام وظایف را می‌بینند. کاربران عادی وظایف اختصاص‌داده‌شده به خودشان یا ایجادشده توسط خودشان را می‌بینند.
*   **کوئری:**
    ```graphql
    query GetAllTasks {
      allTasks {
        id
        title
        status
        priority
        dueDate
        assignedTo {
          username
        }
        createdBy {
          username
        }
        subtasks {
          id
          title
          status
        }
      }
    }
    ```

### 2. دریافت وظایف من (MyTasks)
*   **توضیح:** وظایفی که به کاربر لاگین‌شده فعلی اختصاص داده شده‌اند را برمی‌گرداند.
*   **کوئری:**
    ```graphql
    query GetMyAssignedTasks {
      myTasks {
        id
        title
        description
        status
        priority
        dueDate
        createdBy {
          username
        }
      }
    }
    ```

### 3. دریافت یک وظیفه خاص با شناسه (TaskById)
*   **توضیح:** یک وظیفه خاص را با شناسه آن برمی‌گرداند. کاربر باید مدیر، ایجادکننده یا اختصاص‌داده‌شده به آن وظیفه باشد.
*   **کوئری:**
    ```graphql
    query GetSingleTask($taskId: ID!) {
      taskById(id: $taskId) {
        id
        title
        description
        status
        priority
        dueDate
        assignedTo {
          id
          username
          email
        }
        createdBy {
          id
          username
          email
        }
        createdAt
        updatedAt
        subtasks {
          id
          title
          description
          status
        }
      }
    }
    ```
*   **متغیرها (Variables):** (فرض کنید Task ID برابر `"VGFza1R5cGU6Mg=="` است)
    ```json
    {
      "taskId": "VGFza1R5cGU6Mg=="
    }
    ```

### 4. دریافت زیروظیفه‌های یک وظیفه خاص (SubtasksForTask)
*   **توضیح:** تمام زیروظیفه‌های مربوط به یک وظیفه مادر خاص را برمی‌گرداند. دسترسی مشابه دریافت وظیفه با شناسه است.
*   **کوئری:**
    ```graphql
    query GetSubTasks($parentId: ID!) {
      subtasksForTask(taskId: $parentId) {
        id
        title
        description
        status
        createdAt
      }
    }
    ```
*   **متغیرها (Variables):** (فرض کنید Task ID مادر برابر `"VGFza1R5cGU6Mg=="` است)
    ```json
    {
      "parentId": "VGFza1R5cGU6Mg=="
    }
    ```

---

این مثال‌ها باید به شما کمک کنند تا عملکرد API وظایف خود را به طور کامل در Postman تست کنید.
