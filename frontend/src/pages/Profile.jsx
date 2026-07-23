import DashboardLayout from "../layouts/DashboardLayout";

function Profile() {
  return (
    <DashboardLayout>
      <div className="max-w-3xl mx-auto py-8">
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white">Profile Settings</h2>
          <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">Manage your account and preferences</p>
        </div>
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 shadow-sm">
          <div className="flex items-center gap-4">
            <div className="h-16 w-16 rounded-full bg-indigo-100 dark:bg-indigo-900/40 flex items-center justify-center text-indigo-600 dark:text-indigo-400 text-2xl font-bold">
              J
            </div>
            <div>
              <h3 className="text-lg font-medium text-slate-900 dark:text-white">Jitendra</h3>
              <p className="text-sm text-slate-500 dark:text-slate-400">User Account</p>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}

export default Profile;