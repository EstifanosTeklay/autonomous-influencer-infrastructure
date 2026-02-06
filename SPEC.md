# Frontend Specification: Orchestrator Dashboard

**Version:** 1.0  
**Last Updated:** February 6, 2026  
**Framework:** React 18 + TypeScript + Tailwind CSS  
**State Management:** Zustand  
**API Client:** React Query

---

## 1. Application Architecture

### Tech Stack

```
┌─────────────────────────────────────────┐
│         User Browser                     │
├─────────────────────────────────────────┤
│  React 18 (Components)                   │
│  ├─ TypeScript (Type Safety)            │
│  ├─ Tailwind CSS (Styling)              │
│  ├─ Zustand (State)                     │
│  ├─ React Query (Data Fetching)         │
│  └─ Recharts (Visualizations)           │
├─────────────────────────────────────────┤
│  REST API Client                         │
│  WebSocket (Real-time Updates)          │
├─────────────────────────────────────────┤
│  Backend API (FastAPI)                   │
│  PostgreSQL + Redis + Weaviate          │
└─────────────────────────────────────────┘
```

### Directory Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── agents/
│   │   │   ├── AgentCard.tsx
│   │   │   ├── AgentStatusBadge.tsx
│   │   │   └── AgentMetrics.tsx
│   │   ├── campaigns/
│   │   │   ├── CampaignForm.tsx
│   │   │   ├── CampaignList.tsx
│   │   │   └── CampaignGoalTree.tsx
│   │   ├── hitl/
│   │   │   ├── ReviewQueue.tsx
│   │   │   ├── ReviewCard.tsx
│   │   │   └── ContentPreview.tsx
│   │   ├── layout/
│   │   │   ├── Sidebar.tsx
│   │   │   ├── Header.tsx
│   │   │   └── MainLayout.tsx
│   │   └── common/
│   │       ├── Button.tsx
│   │       ├── Card.tsx
│   │       └── LoadingSpinner.tsx
│   ├── pages/
│   │   ├── DashboardPage.tsx
│   │   ├── AgentDetailPage.tsx
│   │   ├── CampaignPage.tsx
│   │   ├── ReviewQueuePage.tsx
│   │   └── SettingsPage.tsx
│   ├── hooks/
│   │   ├── useAgents.ts
│   │   ├── useCampaigns.ts
│   │   └── useReviewQueue.ts
│   ├── stores/
│   │   ├── authStore.ts
│   │   └── uiStore.ts
│   ├── types/
│   │   ├── agent.ts
│   │   ├── campaign.ts
│   │   └── content.ts
│   ├── api/
│   │   ├── client.ts
│   │   ├── agents.ts
│   │   ├── campaigns.ts
│   │   └── hitl.ts
│   └── utils/
│       ├── formatters.ts
│       └── validators.ts
├── public/
├── package.json
├── tsconfig.json
├── tailwind.config.js
└── vite.config.ts
```

---

## 2. Core Pages

### 2.1 Dashboard (Homepage)

**Route:** `/`  
**Purpose:** Fleet-wide overview and real-time monitoring

**Layout:**

```
┌────────────────────────────────────────────────────┐
│  [Logo]  Dashboard    Agents  Campaigns  Review    │  <- Header
├────────────────────────────────────────────────────┤
│                                                     │
│  Fleet Overview                                    │
│  ┌──────────┬──────────┬──────────┬──────────┐   │
│  │ 5 Agents │ 3 Active │ $234 Rev │ $112 Cost│   │  <- KPI Cards
│  │  Active  │Campaigns │  Today   │  Today   │   │
│  └──────────┴──────────┴──────────┴──────────┘   │
│                                                     │
│  Active Agents                                     │
│  ┌────────────────────────────────────────────┐   │
│  │ [Avatar] Ayana                    🟢 Active│   │
│  │ Ethiopian Fashion                          │   │
│  │ ▓▓▓▓▓░░░ Queue: 7 | Budget: 62% | $6.55  │   │  <- Agent Cards
│  ├────────────────────────────────────────────┤   │
│  │ [Avatar] Desta                    🟢 Active│   │
│  │ Tech News                                  │   │
│  │ ▓▓▓░░░░░ Queue: 3 | Budget: 82% | $8.30  │   │
│  └────────────────────────────────────────────┘   │
│                                                     │
│  Review Queue: 4 pending            [View All →]  │
│                                                     │
│  Recent Activity                                   │
│  ┌────────────────────────────────────────────┐   │
│  │ 15:23  Ayana published to Instagram        │   │
│  │ 15:18  Desta awaiting review (Med conf)    │   │  <- Activity Feed
│  │ 15:10  Campaign "Fashion Week" started     │   │
│  └────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────┘
```

**Key Components:**

- `<KPICard>` - Metric display (revenue, costs, agent count)
- `<AgentCard>` - Agent status overview
- `<ActivityFeed>` - Real-time event stream
- `<ReviewQueuePreview>` - Quick access to pending reviews

---

### 2.2 Agent Detail Page

**Route:** `/agents/:agentId`  
**Purpose:** Deep dive into single agent performance

**Wireframe:**

```
┌────────────────────────────────────────────────────┐
│  ← Back to Dashboard                               │
├────────────────────────────────────────────────────┤
│                                                     │
│  [Avatar]  Ayana                      [⏸️ Pause]   │
│  Ethiopian Streetwear Fashion         [⚙️ Edit]    │
│  chimera_fashion_eth_001                           │
│  🟢 Active | Last post: 45 mins ago                │
│                                                     │
│  ┌─────────────────────────────────────────────┐  │
│  │ [Performance] [Content] [Wallet] [Config]   │  │  <- Tabs
│  └─────────────────────────────────────────────┘  │
│                                                     │
│  Performance (7 days)                              │
│  ┌─────────────────────────────────────────────┐  │
│  │ Engagement Rate                              │  │
│  │     %                                        │  │
│  │  8 ┤     ╭──╮                                │  │
│  │  6 ┤   ╭─╯  ╰─╮                              │  │  <- Line Chart
│  │  4 ┤ ╭─╯      ╰──╮                           │  │
│  │  2 ┤─╯            ╰─                         │  │
│  │    └────────────────────                     │  │
│  │    Mon  Tue  Wed  Thu  Fri  Sat  Sun        │  │
│  └─────────────────────────────────────────────┘  │
│                                                     │
│  Current Campaign: Fashion Week Promo              │
│  Budget: $31.20 / $50.00 (62% remaining)          │
│  ▓▓▓▓▓▓░░░░░░                                     │
│                                                     │
│  Recent Posts                                      │
│  ┌──────┬──────┬──────┬──────┐                   │
│  │[IMG] │[IMG] │[IMG] │[IMG] │                   │  <- Content Grid
│  │ 2.3k │ 1.8k │ 3.1k │ 2.6k │                   │
│  │ likes│ likes│ likes│ likes│                   │
│  └──────┴──────┴──────┴──────┘                   │
│                                                     │
└────────────────────────────────────────────────────┘
```

**Key Features:**

- Real-time status indicators
- Performance charts (Recharts)
- Content gallery with metrics
- Wallet balance display
- Quick actions (pause, edit, delete)

---

### 2.3 Campaign Management Page

**Route:** `/campaigns/new`  
**Purpose:** Create and manage campaigns

**Wireframe:**

```
┌────────────────────────────────────────────────────┐
│  Create New Campaign                               │
├────────────────────────────────────────────────────┤
│                                                     │
│  Step 1: Campaign Goal                            │
│  ┌─────────────────────────────────────────────┐  │
│  │ Describe your campaign goal in natural       │  │
│  │ language:                                     │  │
│  │                                               │  │
│  │ [Promote sustainable fashion week in Addis]  │  │  <- AI Goal Input
│  │                                               │  │
│  │            [Generate Task Breakdown →]        │  │
│  └─────────────────────────────────────────────┘  │
│                                                     │
│  Task Breakdown Preview                            │
│  ┌─────────────────────────────────────────────┐  │
│  │ ✓ Research trending sustainable topics       │  │
│  │ ├─ Generate 5 Instagram posts                │  │  <- Task Tree
│  │ ├─ Create 3 TikTok videos                    │  │
│  │ └─ Engage with 50 relevant comments          │  │
│  │                                               │  │
│  │ Estimated: 15 tasks | $38 budget | 5 days    │  │
│  │                                               │  │
│  │ [✏️ Edit] [✓ Approve & Start]                │  │
│  └─────────────────────────────────────────────┘  │
│                                                     │
│  Budget & Schedule                                 │
│  Daily Budget: [$50] per day                      │
│  Duration: [Feb 10] to [Feb 17]                   │
│                                                     │
│  Assigned Agent: [Ayana ▼]                        │
│                                                     │
│                    [Cancel] [Create Campaign]      │
└────────────────────────────────────────────────────┘
```

**Key Features:**

- Natural language goal input
- AI-generated task decomposition preview
- Visual task tree (expandable/collapsible)
- Budget calculator
- Agent selection dropdown

---

### 2.4 HITL Review Queue

**Route:** `/review`  
**Purpose:** Human review of flagged content

**Wireframe:**

```
┌────────────────────────────────────────────────────┐
│  Review Queue                   [Filters ▼]        │
├────────────────────────────────────────────────────┤
│                                                     │
│  4 items pending review                            │
│  Sort by: [Priority ▼]                            │
│                                                     │
│  ┌─────────────────────────────────────────────┐  │
│  │ 🔴 HIGH PRIORITY                             │  │
│  │                                               │  │
│  │ Agent: Ayana                                  │  │
│  │ Task: Instagram post about coffee ceremony   │  │
│  │ Confidence: 0.78 🟡                          │  │
│  │ Flagged: Medium confidence + sensitive topic │  │
│  │                                               │  │
│  │ ┌───────────────────────────────────────┐   │  │
│  │ │ [Preview of Generated Content]         │   │  │  <- Content Preview
│  │ │                                         │   │  │
│  │ │ "The coffee ceremony isn't just about  │   │  │
│  │ │  the brew—it's about connection..."    │   │  │
│  │ │                                         │   │  │
│  │ │ [Image Preview]                        │   │  │
│  │ └───────────────────────────────────────┘   │  │
│  │                                               │  │
│  │ AI Reasoning:                                │  │
│  │ "Generated using cultural storytelling       │  │
│  │  approach. Confidence reduced due to         │  │
│  │  lack of specific designer mentions."        │  │
│  │                                               │  │
│  │ [✓ Approve] [✏️ Edit] [✗ Reject]             │  │  <- Actions
│  │                                               │  │
│  │ Keyboard: A=Approve | E=Edit | R=Reject      │  │
│  └─────────────────────────────────────────────┘  │
│                                                     │
│  [Next Item →]                                     │
└────────────────────────────────────────────────────┘
```

**Key Features:**

- Priority sorting (financial > sensitive > medium confidence)
- Color-coded confidence scores
- Full content preview
- AI reasoning display
- Keyboard shortcuts for speed
- Quick action buttons

---

## 3. Component Specifications

### 3.1 AgentCard Component

**File:** `src/components/agents/AgentCard.tsx`

```typescript
interface AgentCardProps {
  agent: {
    agent_id: string;
    name: string;
    niche: string;
    status: 'active' | 'paused' | 'error';
    queue_depth: number;
    daily_budget_remaining_pct: number;
    profit_today_usd: number;
    last_post_timestamp: string;
  };
  onClick?: () => void;
}

export const AgentCard: React.FC<AgentCardProps> = ({ agent, onClick }) => {
  return (
    <div className="bg-white rounded-lg shadow p-4 hover:shadow-lg transition cursor-pointer" onClick={onClick}>
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-full bg-gradient-to-br from-purple-500 to-pink-500" />
          <div>
            <h3 className="font-semibold text-lg">{agent.name}</h3>
            <p className="text-sm text-gray-600">{agent.niche}</p>
          </div>
        </div>
        <StatusBadge status={agent.status} />
      </div>
      
      <div className="mt-4 grid grid-cols-3 gap-4 text-sm">
        <div>
          <p className="text-gray-500">Queue</p>
          <p className="font-medium">{agent.queue_depth} tasks</p>
        </div>
        <div>
          <p className="text-gray-500">Budget</p>
          <ProgressBar value={agent.daily_budget_remaining_pct} />
        </div>
        <div>
          <p className="text-gray-500">Profit Today</p>
          <p className={`font-medium ${agent.profit_today_usd >= 0 ? 'text-green-600' : 'text-red-600'}`}>
            ${agent.profit_today_usd.toFixed(2)}
          </p>
        </div>
      </div>
      
      <div className="mt-3 text-xs text-gray-500">
        Last post: {formatRelativeTime(agent.last_post_timestamp)}
      </div>
    </div>
  );
};
```

---

### 3.2 ReviewCard Component

**File:** `src/components/hitl/ReviewCard.tsx`

```typescript
interface ReviewCardProps {
  review: {
    review_id: string;
    agent_id: string;
    content_preview: string;
    confidence_score: number;
    reasoning_trace: string;
    flagged_reason: string;
  };
  onApprove: () => void;
  onReject: () => void;
  onEdit: () => void;
}

export const ReviewCard: React.FC<ReviewCardProps> = ({ 
  review, 
  onApprove, 
  onReject, 
  onEdit 
}) => {
  const confidenceColor = 
    review.confidence_score >= 0.9 ? 'bg-green-500' :
    review.confidence_score >= 0.7 ? 'bg-yellow-500' : 
    'bg-red-500';
  
  return (
    <div className="bg-white rounded-lg shadow-lg p-6 border-l-4 border-yellow-400">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="font-semibold">Agent: {review.agent_id}</h3>
          <p className="text-sm text-gray-600">{review.flagged_reason}</p>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-sm text-gray-600">Confidence:</span>
          <div className={`px-3 py-1 rounded-full text-white text-sm ${confidenceColor}`}>
            {(review.confidence_score * 100).toFixed(0)}%
          </div>
        </div>
      </div>
      
      <div className="bg-gray-50 rounded p-4 mb-4">
        <p className="text-sm whitespace-pre-wrap">{review.content_preview}</p>
      </div>
      
      <div className="mb-4">
        <p className="text-xs text-gray-500 mb-1">AI Reasoning:</p>
        <p className="text-sm text-gray-700">{review.reasoning_trace}</p>
      </div>
      
      <div className="flex gap-3">
        <button 
          onClick={onApprove}
          className="flex-1 bg-green-600 hover:bg-green-700 text-white py-2 px-4 rounded font-medium"
        >
          ✓ Approve (A)
        </button>
        <button 
          onClick={onEdit}
          className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded font-medium"
        >
          ✏️ Edit (E)
        </button>
        <button 
          onClick={onReject}
          className="flex-1 bg-red-600 hover:bg-red-700 text-white py-2 px-4 rounded font-medium"
        >
          ✗ Reject (R)
        </button>
      </div>
    </div>
  );
};
```

---

## 4. State Management

### 4.1 Auth Store (Zustand)

**File:** `src/stores/authStore.ts`

```typescript
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface AuthState {
  user: {
    user_id: string;
    email: string;
    role: string;
  } | null;
  token: string | null;
  
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: () => boolean;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      
      login: async (email, password) => {
        const response = await fetch('/api/v1/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password })
        });
        
        const data = await response.json();
        set({ user: data.user, token: data.token });
      },
      
      logout: () => {
        set({ user: null, token: null });
      },
      
      isAuthenticated: () => {
        return !!get().token;
      }
    }),
    { name: 'auth-storage' }
  )
);
```

---

## 5. API Integration

### 5.1 Agents API Client

**File:** `src/api/agents.ts`

```typescript
import { apiClient } from './client';

export interface Agent {
  agent_id: string;
  name: string;
  niche: string;
  status: 'active' | 'paused' | 'archived';
  wallet_address: string;
  daily_budget_usd: number;
  // ... more fields
}

export const agentsApi = {
  getAll: async (): Promise<Agent[]> => {
    const { data } = await apiClient.get('/agents');
    return data;
  },
  
  getById: async (id: string): Promise<Agent> => {
    const { data } = await apiClient.get(`/agents/${id}`);
    return data;
  },
  
  getStatus: async (id: string) => {
    const { data } = await apiClient.get(`/agents/${id}/status`);
    return data;
  },
  
  pause: async (id: string) => {
    const { data } = await apiClient.post(`/agents/${id}/pause`);
    return data;
  },
  
  resume: async (id: string) => {
    const { data} = await apiClient.post(`/agents/${id}/resume`);
    return data;
  }
};
```

---

## 6. Real-time Updates

### WebSocket Integration

**File:** `src/hooks/useRealtimeUpdates.ts`

```typescript
import { useEffect } from 'react';
import { useQueryClient } from '@tanstack/react-query';

export const useRealtimeUpdates = (agentId?: string) => {
  const queryClient = useQueryClient();
  
  useEffect(() => {
    const ws = new WebSocket(`ws://localhost:8000/ws/${agentId || 'all'}`);
    
    ws.onmessage = (event) => {
      const update = JSON.parse(event.data);
      
      // Invalidate queries to refetch fresh data
      if (update.type === 'agent_status_changed') {
        queryClient.invalidateQueries(['agents', update.agent_id]);
      }
      
      if (update.type === 'content_published') {
        queryClient.invalidateQueries(['content', update.agent_id]);
      }
      
      if (update.type === 'review_queued') {
        queryClient.invalidateQueries(['hitl-queue']);
      }
    };
    
    return () => ws.close();
  }, [agentId, queryClient]);
};
```

---

## 7. Responsive Design

### Breakpoints

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    screens: {
      'sm': '640px',   // Mobile
      'md': '768px',   // Tablet
      'lg': '1024px',  // Desktop
      'xl': '1280px',  // Large Desktop
    }
  }
}
```

### Mobile-First Approach

```tsx
// Components adapt to screen size
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {agents.map(agent => <AgentCard key={agent.agent_id} agent={agent} />)}
</div>
```

---

## 8. Accessibility

### WCAG 2.1 AA Compliance

- All interactive elements keyboard navigable
- ARIA labels on icons and buttons
- Color contrast ratio ≥ 4.5:1
- Screen reader friendly

```tsx
<button
  aria-label="Approve content"
  className="focus:outline-none focus:ring-2 focus:ring-green-500"
>
  ✓ Approve
</button>
```

---

## 9. Performance Optimization

### Code Splitting

```tsx
// Lazy load pages
const DashboardPage = lazy(() => import('./pages/DashboardPage'));
const AgentDetailPage = lazy(() => import('./pages/AgentDetailPage'));
```

### Query Caching

```tsx
// React Query cache configuration
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000, // 1 minute
      cacheTime: 5 * 60 * 1000, // 5 minutes
      refetchOnWindowFocus: false
    }
  }
});
```

---

## 10. Testing Strategy

### Component Tests

```tsx
// src/components/agents/__tests__/AgentCard.test.tsx
import { render, screen } from '@testing-library/react';
import { AgentCard } from '../AgentCard';

describe('AgentCard', () => {
  it('displays agent name and niche', () => {
    const agent = {
      agent_id: 'test_001',
      name: 'Test Agent',
      niche: 'Test Niche',
      status: 'active',
      // ...
    };
    
    render(<AgentCard agent={agent} />);
    
    expect(screen.getByText('Test Agent')).toBeInTheDocument();
    expect(screen.getByText('Test Niche')).toBeInTheDocument();
  });
  
  it('shows green status badge when active', () => {
    // Test implementation
  });
});
```

---

## 11. Deployment

### Build Configuration

```json
// package.json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "test": "vitest",
    "lint": "eslint src --ext .ts,.tsx"
  }
}
```

### Environment Variables

```bash
# .env
VITE_API_URL=http://localhost:8000/api/v1
VITE_WS_URL=ws://localhost:8000/ws
VITE_AUTH_ENABLED=true
```

---

## 12. Future Enhancements

### Phase 2:
- Mobile app (React Native)
- Advanced analytics dashboards
- A/B test management UI
- Collaborative editing for campaigns

### Phase 3:
- Voice commands for reviews
- AR preview for content
- Multi-language support
- White-label customizatio
