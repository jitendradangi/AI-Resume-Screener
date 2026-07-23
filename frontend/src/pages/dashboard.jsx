import DashboardLayout from "../layouts/DashboardLayout";

function Dashboard() {
  return (
    <DashboardLayout>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Dashboard</h1>
        <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">Welcome to AI Resume Screener.</p>
      </div>
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
         <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 shadow-sm">
           <h3 className="text-sm font-medium text-slate-500 dark:text-slate-400">Total Resumes</h3>
           <p className="mt-2 text-3xl font-bold text-slate-900 dark:text-white">0</p>
         </div>
         <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 shadow-sm">
           <h3 className="text-sm font-medium text-slate-500 dark:text-slate-400">Avg. ATS Score</h3>
           <p className="mt-2 text-3xl font-bold text-slate-900 dark:text-white">-</p>
         </div>
      </div>
    </DashboardLayout>
  );
}

export default Dashboard;