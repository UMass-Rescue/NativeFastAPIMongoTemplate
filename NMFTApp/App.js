import React from "react";
import { StyleSheet, Text, View, Button, TextInput } from "react-native";
import axios from "axios";
import { v4 as uuid } from "uuid";

const { BlobServiceClient } = require("@azure/storage-blob");

const server_url = "http://localhost:8000/";
const example_worker_endpoint = server_url + "predict_worker_example/";

const blobSasUrl =
  "https://jagathrescue.blob.core.windows.net/596e-backend?sp=racwdli&st=2022-03-02T18:39:33Z&se=2022-06-02T01:39:33Z&spr=https&sv=2020-08-04&sr=c&sig=7hdLnsjVUTPNmfzV2RJBkZdUP%2BrkVKrWlcEibwvKeIA%3D";
const blobContainer = "596e-backend";

export default function App() {
  const [text, onChangeText] = React.useState("Click me to change text");
  const [prediction, setPrediction] = React.useState("");
  const blobServiceClient = new BlobServiceClient(blobSasUrl);
  const containerClient = blobServiceClient.getContainerClient(blobContainer);

  const getExampleResult = async (text) => {
    const blob_key = uuid();
    const blockBlobClient = containerClient.getBlockBlobClient(blob_key);
    await blockBlobClient.upload(Buffer.from(text), text.length);

    axios
      .post(example_worker_endpoint, {
        blob_key: blob_key,
      })
      .then((response) => {
        console.log(response.data);
        setPrediction(JSON.stringify(response.data));
      });
  };

  return (
    <View style={styles.container}>
      <TextInput
        style={styles.input}
        onChangeText={onChangeText}
        value={text}
      />
      <br />
      <Button
        onPress={async () => {
          getExampleResult(text);
        }}
        title="Get Prediction"
        color="#841584"
      />
      <br />
      <Text>{prediction}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center",
  },
});
