
#ifndef P2PSP_CORE_PEER_IMS_H
#define P2PSP_CORE_PEER_IMS_H

#include <vector>
#include <string>
#include <memory>

namespace p2psp {

class PeerIMS {
  // Default port used to serve the player.
  static const unsigned short kPlayerPort = 9999;

  // Default address of the splitter.
  constexpr static const char kSplitterAddr[] = "127.0.0.1";

  // Default port of the splitter.
  static const unsigned short kSplitterPort = 4552;

  // Default TCP->UDP port used to communicate.
  static const unsigned short kPort = 0;

  // Default use localhost instead the IP of the addapter
  static const bool kUseLocalhost = false;

  // Default ?
  static const int kBufferStatus = 0;

  // Default
  static const bool kShowBuffer = false;

  // Port used to serve the player.
  unsigned short player_port;

  // Address of the splitter.
  std::string splitter_addr;

  // Port of the splitter.
  unsigned short splitter_port;

  // TCP->UDP port used to communicate.
  unsigned short port;

  // Use localhost instead the IP of the addapter
  bool use_localhost;

  // ?
  int buffer_status;

  bool show_buffer;

  unsigned int buffer_size_;
  unsigned int chunk_size_;
  std::vector<char> chunks_;
  unsigned int header_size_in_chunks_;
  std::string mcast_addr_;
  unsigned short mcast_port_;
  unsigned int message_format_;
  std::shared_ptr<char> played_chunk_;  // Dynamic pointer
  bool player_alive_;
  int player_socket_;
  unsigned int received_counter_;
  std::vector<bool> received_flag_;
  unsigned int recvfrom_counter_;
  unsigned int splitter_;
  int splitter_socket_;
  int team_socket_;

 public:
  PeerIMS();
  ~PeerIMS();

  /**
   *  Setup "player_socket" and wait for the player
   */
  void WaitForThePlayer();

  /**
   *  Setup "splitter" and "splitter_socket"
   */
  void ConnectToTheSplitter();
  void DisconnectFromTheSplitter();
  void ReceiveTheMcasteEndpoint();
  void ReceiveTheHeader();
  void ReceiveTheChunkSize();
  void ReceiveTheHeaderSize();
  void ReceiveTheBufferSize();

  /**
   *  Create "team_socket" (UDP) for using the multicast channel
   */
  void ListenToTheTeam();
  void UnpackMessage();  // TODO: (message)
  void ReceiveTheNextMessage();
  void ProcessMessage();  // TODO: (message, sender)
  void ProcessNextMessage();

  /**
   *  Buffering
   */
  void BufferData();
  void FindNextChunk();
  void PlayChunk();
  void PlayNextChunk();  // TODO: (chunk)
  void Play();
  void KeepTheBufferFull();
  void Run();
};
}

#endif  // P2PSP_CORE_PEER_IMS_H
