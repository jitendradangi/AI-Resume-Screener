import DashboardLayout from "../layouts/DashboardLayout";

function ATSScore() {
  return (
    <DashboardLayout>
      <div className="max-w-4xl mx-auto py-8">
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white">ATS Score</h2>
          <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">Analyze your resume against job descriptions</p>
        </div>
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-12 text-center shadow-sm">
          <h3 className="text-lg font-medium text-slate-900 dark:text-white">Coming Soon</h3>
          <p className="mt-2 text-slate-500 dark:text-slate-400">The ATS scoring feature is currently under development.</p>
        </div>
      </div>
    </DashboardLayout>
  );
}

export default ATSScore;