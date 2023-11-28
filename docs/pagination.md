# Huma-SDK Pagination Documentation

This guide provides comprehensive information on the pagination features offered by the SDK, outlining two distinct methods for navigating through large sets of data.

## 1. Traditional Pagination

### Overview

Traditional pagination involves the use of standard query parameters to retrieve a specific subset of records from your REST API.

### Parameters

- **page:** Integer specifying the page number.
- **limit:** Integer defining the number of records per page.

### Example Usage

```bash
GET /api/data?page=2&limit=10
```

In this example, the request fetches records from page 2 with a limit of 10 records per page.

## 2. Aggregated Pages Results

### Overview

Aggregated Pages Results is an innovative pagination method that allows the retrieval of multiple pages in a single function call.

### Parameters

- **page:** Integer specifying the starting page for the batch.
- **limit:** Integer defining the number of records per page.
- **is_batch_pages:** Boolean flag indicating whether batch pagination should be applied.
- **max_page_count:** Integer specifying the maximum number of pages to be returned in the batch.

#### Usage of `page` Parameter in Batch Pagination with `max_page_count`
When utilizing batch pagination, the page parameter specifies the starting page within the batch, and in conjunction with max_page_count, determines the total number of pages to be fetched.

### Example Usage

```bash
GET /api/data?page=6&limit=10&is_batch_pages=true&max_page_count=10
```

In this example, the request returns records starting from page 6, with a limit of 10 records per page, utilizing batch pagination. The maximum number of pages returned in the batch is set to 10.

### Note

- **Batch Wait Time:** There is a 5-second wait between successive requests for batch pagination.

