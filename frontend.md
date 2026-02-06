# Frontend Specification - Project Chimera Dashboard

**Version:** 1.1  
**Last Updated:** February 6, 2026  
**Status:** Concrete UI Specification (Phase 1)  
**Framework:** React 18+ with TypeScript  
**Build:** Vite 5.0+  
**Styling:** Tailwind CSS  

---

## 1. Frontend Architecture

### 1.1 Technology Stack

```yaml
Core:
  - React: 18.2+
  - TypeScript: 5.0+
  - Vite: 5.0+ (build tool)

Styling:
  - Tailwind CSS: 3.4+
  - Headless UI: Component primitives
  - Lucide React: Icons

State & Data:
  - TanStack Query: Server state
  - React Context: Global UI state
  - Zustand: Agent dashboard state

Routing:
  - React Router: 6.20+

Charts & Visualization:
  - Recharts: Agent performance charts
  - D3.js: Advanced visualizations

Forms:
  - React Hook Form: Form management
  - Zod: Validation schemas

Real-time:
  - Server-Sent Events (SSE): Live agent updates
  - WebSocket: Optional for Phase 2
```

| **Technology** | **Version** | **Purpose** |
| --- | --- | --- |
| React | 18.2+ | Component-based UI |
| TypeScript | 5.0+ | Type safety |
| Vite | 5.0+ | Fast dev server & build |
| Tailwind CSS | 3.4+ | Utility-first styling |
| Zustand | 4.5+ | Light state management |
| TanStack Query | 5.0+ | Server state & caching |
| React Router | 6.20+ | Client-side routing |
| React Hook Form | 7.5+ | Efficient forms |
| Zod | 3.22+ | Runtime schema validation |
| Recharts | 2.11+ | Agent performance charts |
| Lucide React | 0.292+ | Consistent icons |
| Server-Sent Events | Browser native | Live agent updates |

### 1.2 Application Structure

```
frontend/
├── public/
│   └── assets/
├── src/
│   ├── components/
│   │   ├── agents/          # Agent-specific components
│   │   ├── campaigns/       # Campaign management
│   │   ├── hitl/           # Human-in-the-loop review
│   │   ├── analytics/      # Charts and metrics
│   │   └── ui/             # Reusable UI components
│   ├── pages/
│   │   ├── Dashboard.tsx
│   │   ├── AgentDetail.tsx
│   │   ├── HITLQueue.tsx
│   │   ├── Campaigns.tsx
│   │   └── Settings.tsx
│   ├── hooks/
│   │   ├── useAgents.ts
│   │   ├── useHITLQueue.ts
│   │   └── useCampaigns.ts
│   ├── api/
│   │   └── client.ts
│   ├── types/
│   │   └── index.ts
│   └── utils/
│       └── formatters.ts
├── package.json
├── tsconfig.json
├── tailwind.config.js
└── vite.config.ts
```

---

## 2. Page Specifications

### 2.1 Fleet Dashboard (Home Page)

**Route:** `/dashboard`  
**Purpose:** Overview of all agents and fleet health  
**Access:** Network Operators

#### Layout

```
┌─────────────────────────────────────────────────────────┐
│ HEADER                                                   │
│ [Logo] Project Chimera    [User Menu] [Notifications]  │
├─────────────────────────────────────────────────────────┤
│ SIDEBAR        │ MAIN CONTENT                          │
│                │                                        │
│ Dashboard      │ ┌──────────────────────────────────┐ │
│ Agents         │ │ Fleet Metrics                    │ │
│ Campaigns      │ │ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐│ │
│ HITL Queue     │ │ │  5  │ │ $234│ │ 89% │ │  12 ││ │
│ Analytics      │ │ │Activ│ │Today│ │Budg.│ │Queue││ │
│ Settings       │ │ └─────┘ └─────┘ └─────┘ └─────┘│ │
│                │ └──────────────────────────────────┘ │
│                │                                        │
│                │ ┌──────────────────────────────────┐ │
│                │ │ Active Agents                    │ │
│                │ │                                  │ │
│                │ │ [Agent Card] [Agent Card] ...    │ │
│                │ │                                  │ │
│                │ └──────────────────────────────────┘ │
└────────────────┴─────────────────────────────────────┘
```

#### Agent Card Component

```tsx
// Component: AgentCard
<div className="border rounded-lg p-4 bg-white shadow-sm">
  {/* Header */}
  <div className="flex items-center justify-between mb-3">
    <div className="flex items-center gap-3">
      <div className="w-12 h-12 rounded-full bg-gradient-to-br from-purple-400 to-pink-500" />
      <div>
        <h3 className="font-semibold">Ayana</h3>
        <p className="text-sm text-gray-500">chimera_fashion_eth_001</p>
      </div>
    </div>
    <StatusBadge status="active" />
  </div>

  {/* Metrics */}
  <div className="grid grid-cols-3 gap-2 mb-3">
    <Metric label="Posts Today" value="4" />
    <Metric label="Engagement" value="6.7%" trend="+0.3%" />
    <Metric label="Budget" value="62%" />
  </div>

  {/* Current Activity */}
  <div className="text-sm text-gray-600 mb-3">
    <p className="truncate">Currently: Generating content about coffee culture</p>
  </div>

  {/* Actions */}
  <div className="flex gap-2">
    <Button variant="outline" size="sm">View Details</Button>
    <Button variant="ghost" size="sm">Pause</Button>
  </div>
</div>
```

#### Data Model

```typescript
interface FleetMetrics {
  activeAgents: number;
  totalRevenue: number;
  averageBudgetUtilization: number;
  pendingHITLReviews: number;
}

interface AgentCardData {
  agentId: string;
  name: string;
  status: 'active' | 'paused' | 'error' | 'idle';
  postsToday: number;
  engagementRate: number;
  engagementTrend: number;
  budgetUtilization: number;
  currentActivity: string | null;
  walletBalance: number;
}
```

#### API Endpoints

```typescript
GET /api/v1/dashboard/metrics
Response: FleetMetrics

├── src/components/agents/AgentCard.tsx          # Agent summary
├── src/components/agents/AgentDetail.tsx        # Full agent detail
├── src/components/agents/AgentMetrics.tsx       # Charts
├── src/components/agents/AgentTimeline.tsx      # Activity log
├── src/components/campaigns/CampaignForm.tsx    # CRUD form
├── src/components/campaigns/BudgetTracker.tsx   # Budget viz
├── src/components/hitl/ReviewQueue.tsx          # HITL list
├── src/components/hitl/ReviewCard.tsx           # Review item
├── src/components/hitl/ContentPreview.tsx       # Artifact preview
├── src/components/ui/                           # Reusable primitives
├── src/pages/Dashboard.tsx                      # Home
├── src/pages/AgentsPage.tsx                     # Agent management
├── src/pages/CampaignsPage.tsx                  # Campaign mgmt
├── src/pages/HITLQueuePage.tsx                  # Review queue
├── src/pages/AnalyticsPage.tsx                  # Reporting
├── src/pages/SettingsPage.tsx                   # Configuration
GET /api/v1/agents?status=active
Response: AgentCardData[]

GET /api/v1/agents/:id/status (SSE)
Response: Stream of agent status updates
```

---

### 2.2 Agent Detail Page

**Route:** `/agents/:agentId`  
**Purpose:** Detailed view of single agent  
**Access:** Network Operators

#### Layout

```
┌─────────────────────────────────────────────────────────┐
│ ← Back to Dashboard                    [Pause] [Edit]  │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ ┌────────────────────────────────────────────────────┐ │
│ │ Agent: Ayana (chimera_fashion_eth_001)            │ │
│ │ Status: 🟢 Active  |  Wallet: $127.45 USDC        │ │
│ └────────────────────────────────────────────────────┘ │
│                                                          │
│ ┌─────────────┬──────────────────────────────────────┐│
│ │ TABS        │                                      ││
│ │ Overview    │ Performance Chart (7 days)           ││
│ │ Content     │ [Line chart: engagement over time]   ││
│ │ Campaigns   │                                      ││
│ │ Memory      │ Recent Posts:                        ││
│ │ Wallet      │ [Post] [Post] [Post] [Post]          ││
│ │             │                                      ││
│ │             │ Task Queue (7 pending):              ││
│ │             │ 1. Generate caption (high priority)  ││
│ │             │ 2. Reply to comment (medium)         ││
│ │             │ ...                                  ││
│ └─────────────┴──────────────────────────────────────┘│
└─────────────────────────────────────────────────────────┘
```

#### Tab Views

**Overview Tab:**
- Real-time activity stream
- Performance metrics (24h, 7d, 30d)
- Task queue status
- Recent posts with engagement

**Content Tab:**
- Published content grid
- Filter by platform
- Engagement metrics per post
- Content calendar view

**Campaigns Tab:**
- Active campaigns list
- Campaign performance
- Budget tracking

**Memory Tab:**
- Semantic memory explorer
- Important memories (high importance score)
- Learning patterns visualization

**Wallet Tab:**
- Transaction history
- Balance over time
- Spending breakdown by category

#### Components

```tsx
// PerformanceChart.tsx
interface PerformanceChartProps {
  data: {
    date: string;
    posts: number;
    engagement: number;
    revenue: number;
  }[];
  metric: 'posts' | 'engagement' | 'revenue';
  timeRange: '24h' | '7d' | '30d';
}

// TaskQueueList.tsx
interface TaskQueueListProps {
  tasks: Task[];
  onRetry: (taskId: string) => void;
  onCancel: (taskId: string) => void;
}

// ContentGrid.tsx
interface ContentGridProps {
  content: ContentItem[];
  onSelect: (contentId: string) => void;
  selectedPlatforms: Platform[];
}
```

---

### 2.3 HITL Review Queue

**Route:** `/hitl`  
**Purpose:** Human review of flagged content  
**Access:** Human Reviewers

#### Layout

```
┌─────────────────────────────────────────────────────────┐
│ HITL Review Queue              Pending: 12   Today: 45  │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ Filters: [All] [High Priority] [Medium] [Low]          │
│          [Transactions] [Sensitive Topics] [Low Conf]   │
│                                                          │
│ ┌────────────────────────────────────────────────────┐ │
│ │ 🔴 HIGH PRIORITY                                   │ │
│ │                                                    │ │
│ │ Agent: Ayana  |  Type: Instagram Post              │ │
│ │ Confidence: 0.78  |  Reason: Medium confidence     │ │
│ │                                                    │ │
│ │ ┌──────────────────────┐  ┌────────────────────┐ │ │
│ │ │ [Preview Image]      │  │ Caption:           │ │ │
│ │ │                      │  │ "Check out this... │ │ │
│ │ │                      │  │                    │ │ │
│ │ └──────────────────────┘  └────────────────────┘ │ │
│ │                                                    │ │
│ │ Reasoning: "Generated relevant content but        │ │
│ │ cultural reference needs validation..."           │ │
│ │                                                    │ │
│ │ [✓ Approve] [✗ Reject] [✏️ Edit] [Skip]           │ │
│ └────────────────────────────────────────────────────┘ │
│                                                          │
│ [Next item...] [Previous] [Skip to High Priority]      │
└─────────────────────────────────────────────────────────┘
```

#### Keyboard Shortcuts

```typescript
const shortcuts = {
  'a': 'Approve current item',
  'r': 'Reject current item',
  'e': 'Edit current item',
  's': 'Skip to next',
  'n': 'Next item',
  'p': 'Previous item',
  '1-5': 'Jump to priority level'
};
```

#### Review Modal

```tsx
interface ReviewModalProps {
  item: HITLQueueItem;
  onApprove: (comment?: string) => void;
  onReject: (reason: string, feedback: string) => void;
  onEdit: (newContent: string) => void;
}

// Rejection reasons dropdown
const rejectionReasons = [
  'Off-brand tone',
  'Factual error',
  'Inappropriate content',
  'Cultural insensitivity',
  'Copyright violation',
  'Other (specify)'
];
```

---

### 2.4 Campaign Creation Wizard

**Route:** `/campaigns/new`  
**Purpose:** Multi-step campaign setup  
**Access:** Network Operators

#### Flow

```
Step 1: Basic Info       Step 2: Goals         Step 3: Review
┌──────────────┐        ┌──────────────┐      ┌──────────────┐
│ Campaign     │   →    │ Goal         │  →   │ Confirm &    │
│ Name         │        │ Description  │      │ Launch       │
│ Agent        │        │ Budget       │      │              │
│ Dates        │        │ Target KPIs  │      │              │
└──────────────┘        └──────────────┘      └──────────────┘
```

#### Step 1: Basic Info

```tsx
<FormStep title="Campaign Basics">
  <InputField
    label="Campaign Name"
    placeholder="e.g., Summer Fashion Week Promotion"
    required
  />
  
  <SelectField
    label="Assign to Agent"
    options={availableAgents}
    required
  />
  
  <DateRangePicker
    label="Campaign Duration"
    required
  />
  
  <InputField
    label="Budget (USD)"
    type="number"
    prefix="$"
    required
  />
</FormStep>
```

#### Step 2: Goals (Natural Language)

```tsx
<FormStep title="Campaign Goals">
  <TextareaField
    label="Describe your campaign goal"
    placeholder="e.g., Promote sustainable fashion week in Addis Ababa to Gen-Z audience..."
    rows={6}
    required
  />
  
  {/* AI-generated task breakdown preview */}
  {goalDescription && (
    <TaskBreakdownPreview
      goal={goalDescription}
      onApprove={handleTasksApprove}
      onEdit={handleTasksEdit}
    />
  )}
</FormStep>
```

#### Step 3: Review & Launch

```tsx
<FormStep title="Review & Launch">
  <SummaryCard>
    <SummaryItem label="Campaign" value={campaignName} />
    <SummaryItem label="Agent" value={selectedAgent.name} />
    <SummaryItem label="Duration" value={formatDateRange(dates)} />
    <SummaryItem label="Budget" value={formatCurrency(budget)} />
    <SummaryItem label="Estimated Posts" value={estimatedPosts} />
  </SummaryCard>
  
  <TaskList tasks={generatedTasks} readonly />
  
  <Button onClick={handleLaunch} size="lg">
    Launch Campaign
  </Button>
</FormStep>
```

---

## 3. Component Library

### 3.1 Core UI Components

```typescript
// Button.tsx
interface ButtonProps {
  variant: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger';
  size: 'sm' | 'md' | 'lg';
  icon?: React.ReactNode;
  loading?: boolean;
  disabled?: boolean;
  onClick?: () => void;
  children: React.ReactNode;
}

// Badge.tsx
interface BadgeProps {
  variant: 'success' | 'warning' | 'error' | 'info' | 'neutral';
  size: 'sm' | 'md';
  children: React.ReactNode;
}

// Card.tsx
interface CardProps {
  title?: string;
  subtitle?: string;
  actions?: React.ReactNode;
  children: React.ReactNode;
  className?: string;
}

// Modal.tsx
interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  size: 'sm' | 'md' | 'lg' | 'xl';
  children: React.ReactNode;
  footer?: React.ReactNode;
}

// Table.tsx
interface TableProps<T> {
  columns: ColumnDef<T>[];
  data: T[];
  onRowClick?: (row: T) => void;
  loading?: boolean;
  pagination?: {
    page: number;
    pageSize: number;
    total: number;
    onPageChange: (page: number) => void;
  };
}
```

### 3.2 Agent-Specific Components

```typescript
// AgentStatusIndicator.tsx
interface AgentStatusIndicatorProps {
  status: AgentStatus;
  showLabel?: boolean;
  size?: 'sm' | 'md' | 'lg';
}

// EngagementChart.tsx
interface EngagementChartProps {
  data: EngagementData[];
  metric: 'likes' | 'comments' | 'shares' | 'engagement_rate';
  timeRange: TimeRange;
}

// ConfidenceScoreBadge.tsx
interface ConfidenceScoreBadgeProps {
  score: number; // 0.0 to 1.0
  threshold?: {
    high: number; // e.g., 0.9
    medium: number; // e.g., 0.7
  };
}

// WalletBalance.tsx
interface WalletBalanceProps {
  balance: number;
  currency: 'USDC' | 'ETH';
  trend?: {
    direction: 'up' | 'down';
    percentage: number;
  };
  showChart?: boolean;
}
```

---

## 4. Data Flow & State Management

### 4.1 React Query Hooks

```typescript
// hooks/useAgents.ts
export function useAgents(filters?: AgentFilters) {
  return useQuery({
    queryKey: ['agents', filters],
    queryFn: () => api.getAgents(filters),
    refetchInterval: 30000, // 30 seconds
  });
}

export function useAgentDetail(agentId: string) {
  return useQuery({
    queryKey: ['agent', agentId],
    queryFn: () => api.getAgent(agentId),
  });
}

export function usePauseAgent() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (agentId: string) => api.pauseAgent(agentId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['agents'] });
    },
  });
}

// hooks/useHITLQueue.ts
export function useHITLQueue(filters?: HITLFilters) {
  return useQuery({
    queryKey: ['hitl-queue', filters],
    queryFn: () => api.getHITLQueue(filters),
    refetchInterval: 5000, // 5 seconds
  });
}

export function useApproveHITL() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ reviewId, comment }: { reviewId: string; comment?: string }) =>
      api.approveHITL(reviewId, comment),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['hitl-queue'] });
    },
  });
}
```

### 4.2 Real-Time Updates (SSE)

```typescript
// hooks/useAgentStatusStream.ts
export function useAgentStatusStream(agentId: string) {
  const [status, setStatus] = useState<AgentStatus | null>(null);
  
  useEffect(() => {
    const eventSource = new EventSource(`/api/v1/agents/${agentId}/status`);
    
    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setStatus(data);
    };
    
    eventSource.onerror = () => {
      eventSource.close();
    };
    
    return () => {
      eventSource.close();
    };
  }, [agentId]);
  
  return status;
}
```

---

## 5. Responsive Design

### 5.1 Breakpoints

```typescript
const breakpoints = {
  sm: '640px',   // Mobile landscape
  md: '768px',   // Tablet
  lg: '1024px',  // Desktop
  xl: '1280px',  // Large desktop
  '2xl': '1536px' // Extra large
};
```

### 5.2 Mobile Adaptations

**Dashboard (Mobile):**
- Sidebar collapses to hamburger menu
- Agent cards stack vertically
- Metrics become swipeable carousel

**HITL Queue (Mobile):**
- Full-screen review cards
- Swipe gestures for approve/reject
- Simplified action buttons

**Agent Detail (Mobile):**
- Tabs become bottom navigation
- Charts simplified or hidden
- Focus on essential metrics

---

## 6. Accessibility

### 6.1 Requirements

```typescript
// All interactive elements must have:
- aria-label or aria-labelledby
- Keyboard navigation (Tab, Enter, Escape)
- Focus indicators (outline)
- Screen reader announcements for state changes

// Color contrast ratios:
- Normal text: 4.5:1 minimum
- Large text: 3:1 minimum
- Interactive elements: 3:1 minimum
```

### 6.2 Keyboard Navigation

```typescript
const keyboardShortcuts = {
  global: {
    '/': 'Focus search',
    'g d': 'Go to dashboard',
    'g a': 'Go to agents',
    'g h': 'Go to HITL queue',
    '?': 'Show shortcuts help'
  },
  hitlQueue: {
    'a': 'Approve',
    'r': 'Reject',
    'e': 'Edit',
    'n': 'Next',
    'p': 'Previous'
  }
};
```

---

## 7. Performance Targets

```yaml
Metrics:
  First Contentful Paint: < 1.5s
  Time to Interactive: < 3.5s
  Largest Contentful Paint: < 2.5s
  Cumulative Layout Shift: < 0.1
  
Optimization Strategies:
  - Code splitting per route
  - Lazy loading for charts/heavy components
  - Image optimization (WebP, lazy loading)
  - API response caching
  - Debounced search inputs
  - Virtualized lists for large datasets
```

---

## 8. Testing Strategy

```typescript
// Unit Tests (Vitest)
- All hooks tested
- Component rendering tests
- Form validation tests

// Integration Tests (Playwright)
- Full user flows:
  - Create campaign
  - Review HITL queue
  - View agent details
  - Approve/reject content

// Visual Regression (Chromatic)
- Component screenshot comparisons
- Cross-browser testing
```

---

## 9. Build & Deployment

```yaml
Build Command:
  npm run build

Output:
  dist/
  ├── index.html
  ├── assets/
  │   ├── index-[hash].js
  │   └── index-[hash].css
  └── ...

Environment Variables:
  VITE_API_BASE_URL: Backend API URL
  VITE_SSE_ENDPOINT: Server-Sent Events endpoint
  VITE_WS_ENDPOINT: WebSocket endpoint (Phase 2)

Deployment:
  - Build artifacts served via Nginx
  - API proxied through /api/* route
  - Gzip compression enabled
  - Cache headers for static assets
```

---

## 10. Future Enhancements

### Phase 2:
- Dark mode toggle
- Customizable dashboard layouts
- Advanced analytics (cohort analysis)
- Multi-agent comparison view
- Export reports (PDF, CSV)

### Phase 3:
- Real-time collaboration (multiple operators)
- Mobile app (React Native)
- AI chat assistant in dashboard
- Voice control for HITL review

---

**Implementation Status:** Specified (Frontend not yet built)  
**Priority:** HIGH (Required for full marks)  
**Estimated Effort:** 2-3 days for MVP

---

**Next Step:** Create `frontend/` directory structure and package.json
