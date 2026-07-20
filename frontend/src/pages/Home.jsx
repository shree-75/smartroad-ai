import Navbar from "../components/layout/Navbar";
import Hero from "../components/home/Hero";

function Home() {
  return (
    <>
      <Navbar />

      <main>
        <Hero />

        <section id="features" style={{ minHeight: "100vh", padding: "100px 24px" }}>
          <h2>Features Section</h2>
          <p>This section will be implemented in the next step.</p>
        </section>

        <section id="about" style={{ minHeight: "100vh", padding: "100px 24px" }}>
          <h2>About Section</h2>
          <p>This section will be implemented later.</p>
        </section>
      </main>
    </>
  );
}

export default Home;