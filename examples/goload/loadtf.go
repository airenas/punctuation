package main

import (  
    "fmt"
    "os"
    "bufio"
    "strings"
    "strconv"

    tf "github.com/tensorflow/tensorflow/tensorflow/go"
)

var pMap = map[int32]string{
    0: "",
    1 : ",",
    2 : ".",
    3 : "?",
    4 : "!", 
    5 : ":", 
    6 : ";", 
    7 : "-",
  }

const timesteps = 50
func main() {  
    // working directory must contain:
    // model directory
    modelDir := "m256/1"
    // test file:
    testFile := "test.txt"
    // vocabulary
    vocabFile = "vocabulary"

    model, err := tf.LoadSavedModel(modelDir, []string{"serve"}, nil)
    if err != nil {
        fmt.Printf("Error loading saved model: %s\n", err.Error())
        return
    }
    defer model.Session.Close()
    fmt.Printf("Loaded model\n")

    vocab, err := loadVocab(vocabFile)
    if err != nil {
        fmt.Printf("Error loading vocab: %s\n", err.Error())
        return
    }
    fmt.Printf("Loaded vocab\n")

    data, err := loadString(testFile)
    if err != nil {
        panic(err)
    }
    fmt.Printf("Loaded test data\n")

    dataN := toNum(data, vocab)
    fmt.Printf("Data: %s \n", toJSONString(dataN))
    tensor, err := toTensor(dataN)
    if err != nil {
        panic(err)
    }

    result, err := model.Session.Run(
        map[tf.Output]*tf.Tensor{
            model.Graph.Operation("word_ids").Output(0): tensor, // Replace this with your input layer name
        },
        []tf.Output{
            model.Graph.Operation("lambda/strided_slice").Output(0), // Replace this with your output layer name
        },
        nil,
    )
    fmt.Printf("After run\n")
    
    if err != nil {
        fmt.Printf("Error running the session with input, err: %s\n", err.Error())
        return
    }

    // fmt.Printf("Result value: %v \n", result[0].Value())
    tn := result[0].Value().([][][]float32)
    
    resN := toInt(tn[0])
    fmt.Printf("Prediction: %v \n", resN)
    resTxt := toResult(data, resN)
    fmt.Printf("Result: %v \n", resTxt)
}

func loadString(fn string) ([]string, error) {
    file, err := os.Open(fn)
    if (err != nil){
        return nil, err
    }
    defer file.Close()
    result := make([]string, 0)

    scanner := bufio.NewScanner(file)
    for scanner.Scan() {
        s := scanner.Text()
        strs := strings.Split(s, " ")
        for _, s := range strs {
            s = strings.TrimSpace(s)
            if (s != ""){
                result = append(result, s)    
            }
        }
    }
    return result, nil
}

func toNum(strs []string, vocab map[string]int32) ([]int32) {
    l := len(strs)
    result := make([]int32, 0)
    for i := 0; i < timesteps; i++ {
        s := strs[i % l]
        k, f := vocab[s]
        if !f {
            k = vocab["<UNK>"]             
            
        }
        result = append(result, k)    
    }
    return result
}

func toResult(strs []string, res []int32) string {
    to := len(strs)
    result := ""
    for i, v := range res {
        if (i < to){
            result = result + strs[i]
            p, _ := pMap[v]
            if (p != ""){
                result = result + p                
            }
            result = result + " "    
        }
    }
    return result
}

func toJSONString(inData []int32) string {
    result := ""
    for _, v := range inData {
        result = result +  strconv.Itoa(int(v)) + ","
    }
    return "[" + result + "]"
}

func toInt(res[][]float32) ([]int32) {
    result := make([]int32, 0)
    for _, s := range res {
        result = append(result, argMax(s))    
    }
    return result
}

func toTensor(inData []int32) (*tf.Tensor, error) {
    data := [1][timesteps]int32{}
    for i, v := range inData{
        data[0][i] = v
    }
    return tf.NewTensor(data)
}

func loadVocab(vocabFile string) (map[string]int32, error) {
    file, err := os.Open(vocabFile)
    if (err != nil){
        return nil, err
    }
    defer file.Close()
    result := make(map[string]int32)
    var i int32
    i = 0
    scanner := bufio.NewScanner(file)
    for scanner.Scan() {
        s := scanner.Text()
        result[s] = i
        i++
    }
    return result, nil
}

func argMax(tn []float32) int32 {
    m := float32(-1.0)
    var r int32
    r = 0
    for i, v := range tn{
        if (v > m){
            r = int32(i)
            m = v
        }
    }
    return r
}