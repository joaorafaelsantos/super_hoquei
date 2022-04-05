<script>
  import data from "./data.json";

  let today = data.today;
  let tomorrow = data.tomorrow;
</script>

<main>
  <h1>Super<span>Hóquei</span></h1>
  <details open={!!today.length}>
    <summary>Hoje ({today.length})</summary>
    <div class="row">
      {#each today as game}
        <div class="col">
          <a class="card" href={game.url} target="__blank">
            <h3>{game.home_team} vs {game.away_team}</h3>
            <p>{game.competition}</p>
            <p>{game.date}</p>
          </a>
        </div>
      {/each}
    </div>
  </details>

  <details>
    <summary>Amanhã ({tomorrow.length})</summary>
    <div class="row">
      {#each tomorrow as game}
        <div class="col">
          <a class="card" href={game.url} target="__blank">
            <h3>{game.home_team} vs {game.away_team}</h3>
            <p>{game.competition}</p>
            <p>{game.date}</p>
          </a>
        </div>
      {/each}
    </div>
  </details>
</main>

<style>
  :global(body) {
    background-color: #121212;
    color: hsla(0, 100%, 100%, 0.87);
  }

  main {
    font-family: sans-serif;
  }

  h1 {
    text-align: center;
    font-weight: lighter;
    text-transform: uppercase;
    letter-spacing: -2px;
  }

  h1 span {
    font-weight: bold;
  }

  .row {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
  }

  .col {
    width: 100%;
  }

  details {
    text-align: center;
    margin: 8px 0;
  }

  .card {
    display: inline-block;
    margin: 8px 0;
    border-radius: 10px;
    cursor: pointer;
    width: 100%;
    background-color: rgba(255, 255, 255, 0.05);
    box-shadow: 0px 1px 1px 0px rgb(0 0 0 / 14%),
      0px 2px 1px -1px rgb(0 0 0 / 12%), 0px 1px 3px 0px rgb(0 0 0 / 20%);
  }

  a.card,
  a.card:hover {
    color: hsla(0, 100%, 100%, 0.87);
    text-decoration: none;
  }

  @media (min-width: 480px) {
    .card {
      max-width: 300px;
      padding: 32px;
    }
  }
</style>
