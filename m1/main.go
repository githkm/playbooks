package main

import (
	"flag"
	"github.com/globalsign/mgo"
	"github.com/globalsign/mgo/bson"
	log "github.com/sirupsen/logrus"
	"os"
	"os/signal"
	"strconv"
	"time"
)

func main() {
	var address, db, c string
	flag.StringVar(&address, "address", "127.0.0.1:27017", "mongodb connect address")
	flag.StringVar(&db, "db", "db", "mongodb database name")
	flag.StringVar(&c, "col", "col", "mongodb collection name")
	flag.Parse()
	s := make(chan os.Signal)
	signal.Notify(s)

	err := initClient(address, db)
	if err != nil {
		panic(err)
	}
	err = createCol(c)
	if err != nil {
		panic(err)
	}
	err = ensureIndex(c)
	if err != nil {
		panic(err)
	}

	i := 0
	t := time.After(time.Second)
	log.Infof("start")
	for {
		select {
		case <-t:
			t = time.After(time.Second)
		case <-s:
			log.Infof("stop")
			return
		}
		err = add(c, strconv.Itoa(i), time.Now().Unix())
		if err != nil {
			log.Error(err)
		} else {
			i++
			log.Info(i)
		}
	}
}

var database *mgo.Database

func initClient(address, db string) (err error) {
	session, err := mgo.Dial(address)
	if err != nil {
		return
	}
	database = session.DB(db)
	return
}

func createCol(name string) error {
	return database.C(name).Create(&mgo.CollectionInfo{DisableIdIndex:true})
}

func ensureIndex(name string) error {
	c := database.C(name)
	err := c.EnsureIndex(mgo.Index{
		Key:    []string{"f"},
		Name:   "filename",
		Unique: true,
	})
	if err != nil {
		return err
	}
	err = c.EnsureIndex(mgo.Index{
		Key:    []string{"t"},
		Name:   "timestamp",
		Unique: false,
	})
	return err
}

type Record struct {
	Filename  string `bson:"f"`
	Timestamp int64  `bson:"t"`
}

func add(name string, f string, t int64) error {
	_, err := database.C(name).Upsert(bson.D{{Name: "f", Value: f}}, &Record{Filename: f, Timestamp: t})
	return err
}
