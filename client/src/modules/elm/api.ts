export interface LeaveBalance {
  id: number;
  employee_id: string;
  year: number;
  leave_type: string;
  total_allocated: string;
  used_days: string;
  remaining_days: string;
}

export interface LeaveApplication {
  id: number;
  applicant_id: string;
  leave_type: string;
  start_date: string;
  end_date: string;
  total_days: string;
  is_half_day: boolean;
  reason: string;
  requires_station_leave: boolean;
  station_leave_address: string;
  substitute_id: string;
  status: string;
  reviewer_id: string;
  review_remarks: string;
  created_at: string;
}

export async function fetchMyBalances(): Promise<LeaveBalance[]> {
  const res = await fetch("/api/v1/elm/balances", { credentials: "include" });
  if (!res.ok) throw new Error("Failed to load leave balances");
  return res.json();
}

export async function fetchMyApplications(): Promise<LeaveApplication[]> {
  const res = await fetch("/api/v1/elm/applications", { credentials: "include" });
  if (!res.ok) throw new Error("Failed to load leave applications");
  return res.json();
}

export async function createLeaveApplication(payload: Record<string, unknown>): Promise<LeaveApplication> {
  const res = await fetch("/api/v1/elm/applications", {
    method: "POST",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Failed to submit leave request");
  return res.json();
}
