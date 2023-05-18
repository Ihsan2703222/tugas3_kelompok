const { graphql, buildSchema } = require('graphql');

// Baris ini mengimpor modul graphql dan buildSchema dari paket graphql

// Daftar nama startup
// Ini adalah variabel startups yang berisi array objek yang mewakili startup-startup di Indonesia.
// Setiap objek startup memiliki properti id, name, dan industry.
let startups = [
  { id: 1, name: 'Gojek', industry: 'Ride-hailing' },
  { id: 2, name: 'Tokopedia', industry: 'E-commerce' },
  { id: 3, name: 'Traveloka', industry: 'Travel' },
  { id: 4, name: 'Bukalapak', industry: 'E-commerce' },
  { id: 5, name: 'OVO', industry: 'Fintech' }
];

// Ini adalah definisi skema GraphQL menggunakan buildSchema untuk mendefinisikan tipe-tipe, query, dan mutasi yang didukung.
// Ada tiga tipe yang didefinisikan: Startup yang memiliki properti id, name, dan industry, StartupInput yang digunakan untuk masukan saat menambah dan mengubah startup, Query yang mendefinisikan operasi-query yang dapat dilakukan, dan Mutation yang mendefinisikan operasi-mutasi yang dapat dilakukan.
// startups di dalam Query akan mengembalikan seluruh daftar startup, startup akan mengembalikan informasi tentang startup berdasarkan ID.
// addStartup menerima input dari tipe StartupInput dan menambahkan startup baru ke dalam daftar.
// updateStartup menerima id dan input dari tipe StartupInput dan mengubah startup yang ada dengan ID tersebut.
// deleteStartup menerima id dan menghapus startup dengan ID tersebut.

// Skema GraphQL
const schema = buildSchema(`
  type Startup {
    id: Int
    name: String
    industry: String
  }

  input StartupInput {
    name: String
    industry: String
  }

  type Query {
    startups: [Startup]
    startup(id: Int!): Startup
  }

  type Mutation {
    addStartup(input: StartupInput): Startup
    updateStartup(id: Int!, input: StartupInput): Startup
    deleteStartup(id: Int!): String
  }
`);


// Ini adalah resolver yang mengimplementasikan logika untuk setiap operasi dalam skema.
// Resolver startups mengembalikan seluruh daftar startup.
// Resolver startup mengembalikan informasi tentang startup berdasarkan ID yang diberikan.
// Resolver addStartup menambahkan startup baru ke dalam daftar.
// Resolver updateStartup mengubah informasi startup yang ada berdasarkan ID yang diberikan.
// Resolver deleteStartup menghapus startup berdasarkan ID yang diberikan.
// Resolver GraphQL
const root = {
  startups: () => startups,
  startup: ({ id }) => startups.find(startup => startup.id === id),
  addStartup: ({ input }) => {
    const id = startups.length + 1;
    const newStartup = { id, ...input };
    startups.push(newStartup);
    return newStartup;
  },
  updateStartup: ({ id, input }) => {
    const index = startups.findIndex(startup => startup.id === id);
    if (index !== -1) {
      startups[index] = { id, ...input };
      return startups[index];
    }
    return null;
  },
  deleteStartup: ({ id }) => {
    const index = startups.findIndex(startup => startup.id === id);
    if (index !== -1) {
      const deletedStartup = startups[index];
      startups.splice(index, 1);
      return `Startup "${deletedStartup.name}" deleted successfully`;
    }
    return 'Startup not found';
  }
};

// Bagian ini adalah konfigurasi server Express yang menggunakan express-graphql sebagai middleware untuk menangani permintaan GraphQL.
// Skema (schema) dan resolver (rootValue) yang telah didefinisikan sebelumnya digunakan di sini.
// Server berjalan di port 3000, dan saat dijalankan, Anda akan melihat pesan di konsol yang memberi tahu bahwa server GraphQL telah berjalan.
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
app.listen(8888, () => {
  console.log('Server GraphQL berjalan pada http://localhost:8888/graphql');
});
