
/**
 * Represents the settings for the MongoDB connection.
 * @typedef {Object} MongoSettings
 * @property {string} host - The MongoDB host address.
 * @property {string} db - The name of the MongoDB database.
 * @property {object} opts - Additional options for the MongoDB connection.
 * @property {boolean} opts.useNewUrlParser - Whether to use the new MongoDB connection string parser.
 * @property {boolean} opts.useUnifiedTopology - Whether to use the new MongoDB unified topology engine.
 * @property {number} opts.connectTimeoutMS - The maximum time (in milliseconds) to wait for a connection to be established.
 * @property {number} opts.serverSelectionTimeoutMS - The maximum time (in milliseconds) to wait for a server to be selected.
 */

/**
 * Represents the application settings.
 * @typedef {Object} Settings
 * @property {MongoSettings} mongo - The MongoDB connection settings.
 */
const settings = {
    mongo: /** @type {MongoSettings} */ {
        host: process.env.NODE_ENV == 'development' ? '127.0.0.1' : '10.26.83.142',
        db: 'shows',
        user: null,
        opts: {
            connectTimeoutMS: 5000,
            serverSelectionTimeoutMS: 5000
        },
    }
};

export default settings;