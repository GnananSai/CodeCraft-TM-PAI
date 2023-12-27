const Hero = () => {
  return (
    <div className="hero position-relative">
      <img className="img-fluid" src="./hero.png" alt="" />
      <div className="position-absolute top-0 start-0 p-4">
        <h1>Let Your Reign Begin!</h1>
        <p>Build Your Skills With Courses Tailored For Your Interests</p>
      </div>
    </div>
  );
};

export default Hero;
