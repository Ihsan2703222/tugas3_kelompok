const { graphql, buildSchema } = require('graphql');

// Daftar nama startup
let startups = [
  { id: 1, name: 'Gojek' },
  { id: 2, name: 'Tokopedia' },
  { id: 3, name: 'Traveloka' },
  { id: 4, name: 'Bukalapak' },
  { id: 5, name: 'OVO' }
];

// Skema GraphQL
const schema = buildSchema(`
  type Startup {
    id: Int
    name: String
  }

  type Query {
    startups: [Startup]
    startup(id: Int!): Startup
  }

  type Mutation {
    addStartup(name: String!): Startup
    updateStartup(id: Int!, name: String!): Startup
    deleteStartup(id: Int!): String
  }
`);

// Resolver GraphQL
const root = {
  startups: () => startups,
  startup: ({ id }) => startups.find(startup => startup.id === id),
  addStartup: ({ name }) => {
    const id = startups.length + 1;
    const newStartup = { id, name };
    startups.push(newStartup);
    return newStartup;
  },
  updateStartup: ({ id, name }) => {
    const index = startups.findIndex(startup => startup.id === id);
    if (index !== -1) {
      startups[index].name = name;
      return startups[index];
    }
    return null;
  },
  deleteStartup: ({ id }) => {
    const index = startups.findIndex(startup => startup.id === id);
    if (index !== -1) {
      startups.splice(index, 1);
      return 'Startup deleted successfully';
    }
    return 'Startup not found';
  }
};

// Konfigurasi server
const express = require('express');
const { graphqlHTTP } = require('express-graphql');

const app = express();
app.use('/graphql', graphqlHTTP({
  schema: schema,
  rootValue: root,
  graphiql: true
}));

// Jalankan server
app.listen(3000, () => {
  console.log('Server GraphQL berjalan pada http://localhost:3000/graphql');
});
