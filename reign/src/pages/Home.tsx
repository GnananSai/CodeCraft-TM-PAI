import Hero from "../components/Hero";
import Navbar from "../components/Navbar";

const App = () => {
  return (
    <>
      <div className="app">
        <section>
          <Navbar />
          <Hero />
        </section>
        <section></section>
        <section></section>
        <section></section>
        <section></section>
      </div>
    </>
  );
};

export default App;
