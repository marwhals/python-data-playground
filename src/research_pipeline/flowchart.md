### Paper processing pipeline

---

*Processing pipeline for papers*

```mermaid
graph TD
    A[Start] --> B[Fetch papers from arXiv API]
    B --> C[Parse paper metadata (title, abstract, authors, date)]
    C --> D[Filter by keywords<br/>(e.g., 'survey', 'review')]
    D --> E[Query Semantic Scholar for citation count]
    E --> F{Citation count ≥ threshold?}
    F -- Yes --> G[Add to best paper list]
    F -- No --> H[Discard]
    G --> I[Sort by citation count]
    I --> J[Display top papers with links and summaries]
    J --> K[Optional: Download PDFs]
    K --> L[End]
    H --> L
```