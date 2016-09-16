import kafka.serializer.StringDecoder

import org.apache.spark.streaming._
import org.apache.spark.streaming.kafka._
import org.apache.spark.SparkConf
import org.apache.spark.rdd.RDD
import org.apache.spark.SparkContext
import org.apache.spark.sql._

    case object TransformFunctions extends Serializable {
      val updateFunc = (values: Seq[Int], state: Option[Int]) => {
        val currentCount = values.foldLeft(0)(_ + _)
        val previousCount = state.getOrElse(0)
        Some(currentCount + previousCount)
      }

      // function to convert a timestamp to 5 second time slot
      def convert_to_05sec(timestamp: String): String = {
        val sec05 = timestamp.slice(8,10).toInt/5*5
        timestamp.take(8) + f"${sec05}%02d"
      }
    }

object AhnungStreaming extends Serializable {
  def main(args: Array[String]) {

    val brokers = "ec2-52-44-246-218.compute-1.amazonaws.com:9092"
    val topics = "pipeline1"
    val topicsSet = topics.split(",").toSet

    // Create context with 2 second batch interval
    val sparkConf = new SparkConf().setAppName("ahnung-stream")
    val ssc = new StreamingContext(sparkConf, Seconds(1))
    ssc.checkpoint("hdfs://ec2-52-44-246-218.compute-1.amazonaws.com:9000/user/checkpoint")

    val starttime: Long = System.currentTimeMillis / 1000

    // Create direct kafka stream with brokers and topics
    val kafkaParams = Map[String, String]("metadata.broker.list" -> brokers)
    @transient val messages = KafkaUtils.createDirectStream[String, String, StringDecoder, StringDecoder](ssc, kafkaParams, topicsSet)

    // map each record into a tuple consisting of (URL, UID, epochtime)
    val count = messages
      .map(_._2)
      .map(line => {
        val record = line.split(";")
        (record(0),record(1),record(2))
      })
      .map(record => (TransformFunctions.convert_to_05sec(record._3)))
      .map(record => (record, 1))
      .reduceByKey(_ + _)
      .print()
//      val runningcount = count.updateStateByKey[Int](TransformFunctions.updateFunc)

    // Get the lines and show results
    messages.foreachRDD { rdd =>
      val timestamp: Long = System.currentTimeMillis / 1000

//      runningcount.print()
    }

    // Start the computation
    ssc.start()
    ssc.awaitTermination()
  }
}
