import type { Metadata } from "next";
import styles from "./layout.module.css";

export const metadata: Metadata = {
  title: "Insights Dashboard",
  description: "Financial portfolio insights and asset management dashboard",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={styles.body}>
        <header className={styles.header}>
          <div className={styles.headerContent}>
            <h1>Insights Dashboard</h1>
            <nav className={styles.nav}>
              <a href="/">Insights</a>
              <a href="/assets">Assets</a>
            </nav>
          </div>
        </header>
        <main className={styles.main}>{children}</main>
        <footer className={styles.footer}>
          <p>&copy; 2026 Insights App. All rights reserved.</p>
        </footer>
      </body>
    </html>
  );
}
