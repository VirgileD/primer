import { ObjectId as oid, MongoClient } from 'mongodb';
import settings from './settings.server';

/**
 * Initializes the MongoDB connection.
 * @returns {Promise<import('mongodb').Db>} The MongoDB database instance.
 */
export const init = async () => {
    let auth=""
    let authSource=""
    if("DB_USER" in process.env && "DB_PASSWORD" in process.env) {
        auth = process.env.DB_USER+":"+process.env.DB_PASSWORD+"@"
        // we have set the credential db to be the same as the data db
        authSource=`?authSource=${settings.mongo.db}`
    } else {
        console.log("No DB_USER and DB_PASSWORD set in environment, assuming no authentication")
    }

    const client = await MongoClient.connect(`mongodb://${auth}${settings.mongo.host}/${settings.mongo.db}${authSource}`, settings.mongo.opts);
    const db = client.db(settings.mongo.db);

    return db;
}
export const ObjectId = oid;
