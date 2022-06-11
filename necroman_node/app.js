const exportToLowdb = require('airtable2lowdb')
const fs = require('fs')

//require lowdb and set up db.json as the database
const low = require('lowdb')
const FileSync = require('lowdb/adapters/FileSync')
const adapter = new FileSync('db.json')
const db = low(adapter)

 
console.log("Starting Export...")

db.defaults({skills: [], traits: [], gangers: [], gear:[], tactics: []}).write()

let entities = []



// Export to lowdb
exportToLowdb({
    name: 'Skills', 
    atApiKey: `${AT_KEY}`, 
    baseId: `${NECRO_BASE}`,  
    tables: [                
      'Skills',
    ]
  }).then(results => results['Skills']).then(items => Array.from(items)).then(skills => skills.forEach(item => db.get('skills').push(item).write()))

  exportToLowdb({
    name: 'Traits', 
    atApiKey: `${AT_KEY}`, 
    baseId: `${NECRO_BASE}`,  
    tables: [                
      'Traits',
    ]
  }).then(results => results['Traits']).then(items => Array.from(items)).then(items => items.forEach(item => db.get('traits').push(item).write()))

  exportToLowdb({
    name: 'Territories', 
    atApiKey: `${AT_KEY}`, 
    baseId: `${NECRO_BASE}`,  
    tables: [                
      'Territories',
    ]
  }).then(results => results['Territories']).then(items => Array.from(items)).then(items => items.forEach(item => db.get('terrirories').push(item).write()))


  exportToLowdb({
    name: 'Gang Members', 
    atApiKey: `${AT_KEY}`, 
    baseId: `${NECRO_BASE}`,  
    tables: [                
      'Gang Members',
    ]
  }).then(results => results['Gang Members']).then(items => Array.from(items)).then(items => items.forEach(item => db.get('gangers').push(item).write()))

  exportToLowdb({
    name: 'Tactics', 
    atApiKey: `${AT_KEY}`, 
    baseId: `${NECRO_BASE}`,  
    tables: [                
      'Tactics',
    ]
  }).then(results => results['Tactics']).then(items => Array.from(items)).then(items => items.forEach(item => db.get('tactics').push(item).write()))