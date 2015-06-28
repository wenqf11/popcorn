package cn.edu.tsinghua.thss.popcorn.ui;

import android.app.ProgressDialog;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.support.v4.app.ListFragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.ViewParent;
import android.widget.Button;
import android.widget.FrameLayout;
import android.widget.ListView;
import android.content.Context;
import android.widget.BaseAdapter;
import android.widget.TextView;
import android.widget.Toast;

import com.lidroid.xutils.HttpUtils;
import com.lidroid.xutils.ViewUtils;
import com.lidroid.xutils.exception.HttpException;
import com.lidroid.xutils.http.RequestParams;
import com.lidroid.xutils.http.ResponseInfo;
import com.lidroid.xutils.http.callback.RequestCallBack;
import com.lidroid.xutils.http.client.HttpRequest;
import com.lidroid.xutils.view.annotation.ViewInject;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import org.w3c.dom.Text;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Timer;
import java.util.TimerTask;

import cn.edu.tsinghua.thss.popcorn.MainActivity;
import cn.edu.tsinghua.thss.popcorn.RecordListActivity;
import cn.edu.tsinghua.thss.popcorn.R;
import cn.edu.tsinghua.thss.popcorn.config.Config;



/**
 * @author wenqingfu
 * @date 2015.04.12
 * @email thssvince@163.com
 */

public class RecordFragment extends ListFragment {
    private List<Map<String, Object>> mData;

    String[] mTitle, mTime, mID;

    public int unfinished;

    ProgressDialog progressDialog;

    Handler handler = new Handler() {
        public void handleMessage(Message msg) {
            if (msg.what == 1) {
                //接收消息后要做的处理
                String ROUTE_GET_URL = Config.LOCAL_IP + "/app/route";

                SimpleDateFormat df = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
                String time = df.format(new Date());
                //Timestamp timestamp = Timestamp.valueOf(time);

                RequestParams params = new RequestParams();
                params.addQueryStringParameter("username", Config.DEBUG_USERNAME);
                params.addQueryStringParameter("access_token", Config.ACCESS_TOKEN);
                params.addQueryStringParameter("timestamp", time);

                //progressDialog.show();

                HttpUtils http = new HttpUtils();
                http.configCurrentHttpCacheExpiry(Config.MAX_NETWORK_TIME);
                http.send(HttpRequest.HttpMethod.GET,
                        ROUTE_GET_URL,
                        params,
                        new RequestCallBack<String>() {

                            @Override
                            public void onStart() {
                            }

                            @Override
                            public void onLoading(long total, long current, boolean isUploading) {
                            }

                            @Override
                            public void onSuccess(ResponseInfo<String> responseInfo) {
                                try {
                                    JSONObject jsonObject = new JSONObject(responseInfo.result);
                                    String status = jsonObject.getString("status");
                                    ArrayList<String> tmp_title = new ArrayList<String>();
                                    ArrayList<String> tmp_time = new ArrayList<String>();
                                    ArrayList<String> tmp_route_id = new ArrayList<String>();
                                    if (status.equals("ok")) {
                                        JSONArray results = jsonObject.getJSONArray("data");
                                        for (int i = 0; i < results.length(); ++i) {
                                            JSONObject result = results.getJSONObject(i);
                                            String name = result.getString("name");
                                            String start_time = result.getString("start_time");
                                            String route_id = result.getString("id");
                                            tmp_title.add(name);
                                            tmp_time.add(start_time);
                                            tmp_route_id.add(route_id);
                                        }
                                        mTitle = tmp_title.toArray(new String[]{});
                                        mTime = tmp_time.toArray(new String[]{});
                                        mID = tmp_route_id.toArray(new String[]{});
                                        mData = getData(mTitle, mTime);
                                        RouteListAdapter adapter = new RouteListAdapter(getActivity());
                                        setListAdapter(adapter);
                                        unfinished = mTitle.length;
                                    } else {
                                        //Toast.makeText(getActivity(), "您今天没有抄表任务", Toast.LENGTH_SHORT).show();
                                        unfinished = 0;
                                        //bottomTabMeterText.setText(String.valueOf(1));
                                        //bottomTabMeterText.setText("2");
                                        //bottomTabMeterText.setTextSize(50);
                                        //bottomTabMeterText.setVisibility(View.GONE);
                                    }
                                } catch (JSONException e) {
                                    e.printStackTrace();
                                }
                                //progressDialog.hide();
                            }


                            @Override
                            public void onFailure(HttpException error, String msg) {
                                Toast.makeText(getActivity(), error.getExceptionCode() + ":" + msg, Toast.LENGTH_SHORT).show();
                                //progressDialog.hide();
                            }
                        });
            }
            super.handleMessage(msg);
        };
    };
    Timer timer = new Timer();
    TimerTask task = new TimerTask() {

        @Override
        public void run() {
            // 需要做的事:发送消息
            Message message = new Message();
            message.what = 1;
            handler.sendMessage(message);
        }
    };

	@Override
	public View onCreateView(LayoutInflater inflater,ViewGroup container,Bundle savedInstanceState){
		super.onCreateView(inflater, container, savedInstanceState);
		View recordView = inflater.inflate(R.layout.activity_tab_record, container,false);
        unfinished = 0;
        return recordView;
	}

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        progressDialog = new ProgressDialog(getActivity(), R.style.buffer_dialog);
        progressDialog.setProgressStyle(ProgressDialog.STYLE_SPINNER);
        progressDialog.setMessage("数据加载中...");
        progressDialog.setIndeterminate(false);
        progressDialog.setCancelable(true);

        //String[] str_title = {"线路一","线路二","线路三","线路四","线路五"};
        //String[] str_time = {"8:00","10:00","12:00","14:00","16:00"};
        progressDialog.show();
        timer.schedule(task, 0, Config.RECORD_UPDATE_INTERVAL); // 1s后执行task,经过2s再次执行
        progressDialog.hide();
    }

    @Override
    public void onListItemClick(ListView l, View v, int position, long id) {
        Intent intent = new Intent(getActivity(), RecordListActivity.class);
        Bundle bundle = new Bundle();
        bundle.putString("route_id", mID[(int)id]);
        intent.putExtras(bundle);
        //intent.putExtra("route_id",id);
        startActivity(intent);

        super.onListItemClick(l, v, position, id);
    }

    @Override
	public void onActivityCreated(Bundle savedInstanceState){
		super.onActivityCreated(savedInstanceState);
	}

    private List<Map<String, Object>> getData(String[] str_title, String[] str_time) {
        List<Map<String ,Object>> list = new ArrayList<Map<String,Object>>();

        for (int i = 0; i < str_title.length; i++) {
            Map<String, Object> map = new HashMap<String, Object>();
            map.put("title", str_title[i]);
            map.put("start_time", str_time[i]);
            list.add(map);
        }

        return list;
    }

    class ViewHolder {
        public TextView title;
        public TextView start_time;
    }

    public class RouteListAdapter extends BaseAdapter {
        private LayoutInflater mInflater = null;

        public RouteListAdapter(Context context) {
            super();
            mInflater = (LayoutInflater) context
                    .getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        }

        @Override
        public int getCount() {
            return mData.size();
        }

        @Override
        public Object getItem(int position) {
            // TODO Auto-generated method stub
            return null;
        }

        @Override
        public long getItemId(int position) {
            // TODO Auto-generated method stub
            return position;
        }

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {

            ViewHolder holder = null;
            if (convertView == null) {
                holder = new ViewHolder();
                convertView = mInflater.inflate(R.layout.listview_tab_record, null);
                holder.title = (TextView) convertView.findViewById(R.id.title);
                holder.start_time = (TextView) convertView.findViewById(R.id.start_time);

                convertView.setTag(holder);
            } else {
                holder = (ViewHolder) convertView.getTag();
            }

            holder.title.setText((String)mData.get(position).get("title"));
            holder.start_time.setText((String)mData.get(position).get("start_time"));

            return convertView;
        }
    }
}