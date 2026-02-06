// Frontend Dashboard Page
// See specs/frontend.md for full specification

import { useAgents, useFleetMetrics } from '../hooks/useAgents';
import { AgentCard } from '../components/agents/AgentCard';
import { MetricCard } from '../components/ui/MetricCard';
import { LoadingSpinner } from '../components/ui/LoadingSpinner';

export function Dashboard() {
  const { data: metrics, isLoading: metricsLoading } = useFleetMetrics();
  const { data: agents, isLoading: agentsLoading } = useAgents({ status: 'active' });

  if (metricsLoading || agentsLoading) {
    return <LoadingSpinner />;
  }

  return (
    <div className="p-6">
      {/* Fleet Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <MetricCard
          label="Active Agents"
          value={metrics?.activeAgents ?? 0}
          icon="users"
        />
        <MetricCard
          label="Revenue Today"
          value={`$${metrics?.totalRevenue ?? 0}`}
          icon="dollar-sign"
          trend={+5.2}
        />
        <MetricCard
          label="Budget Usage"
          value={`${metrics?.averageBudgetUtilization ?? 0}%`}
          icon="pie-chart"
        />
        <MetricCard
          label="HITL Queue"
          value={metrics?.pendingHITLReviews ?? 0}
          icon="clock"
          variant={metrics?.pendingHITLReviews > 10 ? 'warning' : 'default'}
        />
      </div>

      {/* Active Agents Grid */}
      <div>
        <h2 className="text-2xl font-bold mb-4">Active Agents</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {agents?.map((agent) => (
            <AgentCard key={agent.agentId} agent={agent} />
          ))}
        </div>
      </div>
    </div>
  );
}

/**
 * IMPLEMENTATION NOTES:
 * - This is a skeleton component following specs/frontend.md §2.1
 * - Full implementation requires:
 *   1. API client setup (see frontend/src/api/client.ts)
 *   2. React Query hooks (see frontend/src/hooks/useAgents.ts)
 *   3. UI components (see frontend/src/components/ui/)
 *   4. Real-time updates via SSE
 * - See specs/frontend.md for complete specifications
 */
